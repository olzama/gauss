(in-package :tsdb)

(defun analyze (data 
                &key condition meter message thorough trees extras 
                     (readerp t) siftp filter output
                     score gold taggingp
		     tokensp commentp inputp sloppyp scorep burst purge)

  (declare (ignore siftp)
           (optimize (speed 1) (safety 3) (space 0))) ; *** (optimize (speed 3) (safety 0) (space 0))

  (let ((virtual (virtual-profile-p data)))
    (when virtual
      (return-from analyze
        (analyze-virtual
         virtual
         :condition condition :meter meter :message message :thorough thorough
         :trees trees :extras extras :readerp readerp
         :filter filter :output output
         :score score :gold gold 
         :taggingp taggingp :tokensp tokensp :commentp commentp :inputp inputp
         :sloppyp sloppyp :scorep scorep :burst burst :purge purge))))
  
  (let* ((message (when message
                    (format nil "retrieving `~a' data ..." data)))
         (extras (and extras t))
         (trees (and trees t))
         (filter (when (and filter
                            (functionp *statistics-result-filter*)
                            *filter-test*)
                   (format 
                    nil
                    "~{~(~a~)~^+~}~@[+~a~]"
                    *filter-test* *filter-mrs-relations-ratio*)))
         (key (format 
               nil 
               "~a~@[ @ ~a~]~@[ # ~a~]~@[~* : comment~]~@[~* : input~]~@[~* : trees~]~@[ for ~a~]~@[~* : extras~]~@[~* : output~]~@[ on ~a~@[ (scores)~]~]" 
               data condition 
               (if (listp thorough) (format nil "~{~(~a~)~^#~}" thorough) "t")
               commentp inputp trees filter extras output
               (cond
                ((stringp score) score)
                (score "itself")
                (gold (format nil "~a (gold)" gold)))
               scorep))
         (relations (read-database-schema data))
         (parse (rest (find "parse" relations :key #'first :test #'string=)))
         (tokensp (and tokensp (>= (profile-granularity data) 201011)))
         pfields ptypes result)
    #+:debug
    (format t "~&analyze(): `~a'~%" key)
    (when message (status :text message))
    (when meter (meter :value (get-field :start meter)))
    ;;
    ;; _fix_me_
    ;; for this to actually be thread-safe, we would need to wrap all writing
    ;; to the profile cache with a process lock.               (16-nov-10; oe)
    ;;
    (loop while (eq (setf result (gethash key *tsdb-profile-cache*)) :seized))
    (unless result
      (setf (gethash key *tsdb-profile-cache*) :seized)
      (loop
          for field 
          in (append '("i-id" "parse-id" "readings" 
                       "first" "total" "tcpu" "tgc"
                       "p-etasks" "p-stasks" "p-ftasks"
                       "unifications" "copies"
                       "conses" "symbols" "others"
                       "words" "l-stasks"
                       "edges" "aedges" "pedges" "raedges" "rpedges"
                       "gcs" "error")
                     (and inputp '("p-input" "p-tokens")))
          for match = (find field parse :key #'first :test #'string=)
          when match do
            (push (first match) pfields)
            (push (second match) ptypes))
      (when extras
        (push "comment" pfields)
        (push :string ptypes))

      (unwind-protect
        ;;
        ;; _fix_me_
        ;; projecting :string fields that contain the field separator (`@') of
        ;; tsdb(1) breaks when used in conjuction with a `report' format (as is
        ;; the case in our current select() implementation.  hence, sort the
        ;; `error' field to the back where it happens not to break :-{.
        ;;                                                      (22-nov-99; oe)
        ;; i believe this has been fixed sometime in 2001?      (20-jan-02; oe)
        ;;          
        (let* ((pfields (nreverse pfields))
               (ptypes (nreverse ptypes))
               (pmeter (and meter (madjust * meter (if thorough 0.4 0.5))))
               (imeter (when meter
                         (madjust + (madjust * meter (if thorough 0.1 0.25)) 
                                  (mduration pmeter))))
               (rmeter (if (and pmeter imeter thorough)
                         (madjust + (madjust * meter 0.4) 
                                  (+ (mduration pmeter) (mduration imeter)))
                         (and meter (make-meter 0 0))))
               (ameter (when meter
                         (madjust + (madjust * meter (if thorough 0.1 0.25)) 
                                  (+ (mduration pmeter) 
                                     (mduration rmeter)
                                     (mduration imeter)))))
               (parse (select pfields ptypes "parse" condition data
                              :meter pmeter :sort :i-id))
               (item (select (append
                              '("i-id" "i-input" "i-length" "i-wf")
                              (when tokensp '("i-tokens"))
                              (when commentp '("i-comment")))
                             (append
                              '(:integer :string :integer :integer)
                              (when tokensp '(:string))
                              (when commentp '(:string)))
                             "item" condition data 
                             :meter imeter :sort :i-id :sourcep t))
	       (item (if (or taggingp tokensp commentp)
                       (loop
                           for foo in item
                           when taggingp do
                             (let* ((i-input (get-field :i-input foo))
                                    (tags (call-raw-hook 
                                           *tsdb-tagging-hook* i-input)))
                               (when tags (nconc foo (acons :tags tags nil))))
                           when tokensp do
                             ;;
                             ;; _hack_
                             ;; see whether the tokens string looks much like
                             ;; an association list; if so, parse that list.
                             ;;
                             (let* ((tokens (get-field :i-tokens foo))
                                    (n (when (stringp tokens)
                                         (- (length tokens) 1))))
                               (if (and n (< 3 n)
                                          (char= (schar tokens 0) #\()
                                          (char= (schar tokens 1) #\()
                                          (char= (schar tokens (- n 1)) #\))
                                          (char= (schar tokens n) #\)))
                                 (let ((tokens (ignore-errors
                                                 (read-from-string tokens))))
                                   (when tokens
                                     (set-field :i-tokens tokens foo)))
                                 (when (equal tokens "")
                                   (set-field :i-tokens nil foo))))
                           when commentp do
                             ;;
                             ;; _hack_
                             ;; see whether the comment string looks much like
                             ;; an association list; if so, parse that list.
                             ;;
                             (let* ((comment (get-field :i-comment foo))
                                    (n (when (stringp comment)
                                         (- (length comment) 1))))
                               (when (and n (< 3 n)
                                          (char= (schar comment 0) #\()
                                          (char= (schar comment 1) #\()
                                          (char= (schar comment (- n 1)) #\))
                                          (char= (schar comment n) #\)))
                                 (let ((comment (ignore-errors
                                                 (read-from-string comment))))
                                   (nconc foo comment))))
                           finally (return item))
		       item))
               (output (when output
                         (if (consp output)
                           (if (member "i-id" output :test #'string-equal)
                             output
                             (cons "i-id" output))
                           '("i-id" "o-ignore" "o-surface"
                             "o-wf" "o-gc" "o-edges"))))
               (outputs (when output
                          (select output nil
                                  "output" condition data
                                  :unique nil :sort :i-id)))
               (results (when thorough
                          ;;
                          ;; _fix_me_
                          ;; for rank-profile() and friends, .conditions. will
                          ;; typically include `readings > 1', or similar; the
                          ;; join of `parse' and `result' in tsdb(1) is really
                          ;; very slow for large relations (because `parse'
                          ;; has multiple keys, and we end up inserting out-
                          ;; of-order :-{).  it would probably pay off to do
                          ;; more of the work on the Lisp side, e.g. select()
                          ;; from `result' unconditionally (which may lead to
                          ;; excessive memory usage), select() from `parse'
                          ;; with .condition., and then njoin().  i should put
                          ;; a little more thought into this!  (29-feb-09; oe)
                          ;;
                          (if burst
                            (let ((parses
                                   (select '("parse-id")
                                    nil "parse" condition data
                                    :sort :parse-id))
                                  (results
                                   (select (append '("parse-id" "result-id")
                                             (loop
                                                 for symbol in thorough
                                                 collect (format 
                                                          nil 
                                                          "~(~a~)" 
                                                          symbol)))
                                    nil "result" nil data
                                    :meter rmeter :sort :parse-id)))
                              (njoin parses results :parse-id))
                            (select (append '("parse-id" "result-id")
                                            (when (consp thorough)
                                              (loop
                                                  for symbol in thorough
                                                  collect (format 
                                                           nil 
                                                           "~(~a~)" 
                                                           symbol))))
                                    nil "result" condition data 
                                    :meter rmeter :sort :parse-id))))
               (trees (when trees
                        (select '("parse-id" "t-active" "t-version")
                                nil "tree" condition data
                                :sort :parse-id)))
               (all (if parse (njoin parse item :i-id :meter ameter) item))
               sorted)
          ;;
          ;; for a subset of top-level fields, call an optional item reader
          ;;
          (loop
              for field in (and inputp '(:p-input :p-tokens))
              for reader = (when (or (and (symbolp readerp) readerp)
                                     (smember field readerp))
                             (find-attribute-reader field))
              when reader
              do
                (loop
                    for item in all
                    for value = (get-field field item)
                    when value do
                      (setf (get-field field item)
                        (ignore-errors (funcall reader value)))))
          (setf result all)
          (when outputs
            (loop
                for item in result
                for iid = (get-field :i-id item)
                for output
                = (loop
                      initially
                        (loop
                            for output = (first outputs)
                            while (and output (< (get-field :i-id output) iid))
                            do (pop outputs))
                      for output = (first outputs)
                      while (and output (= (get-field :i-id output) iid))
                      collect (pop outputs))
                do (nconc item (acons :outputs output nil))))
          (when extras
            (loop
                for tuple in result
                for comment = (get-field :comment tuple)
                for stream = (when (and (stringp comment) (> (length comment) 0)
                                        (char= (char comment 0) #\())
                               (make-string-input-stream comment))
                for extra = (when stream
                              (loop
                                  for field = (ignore-errors (read stream nil nil))
                                  while field
                                  collect field
                                  finally (close stream)))
                when extra do
                  (nconc tuple extra)))
          (when results
            (when (consp thorough)
              (loop
                  for field in thorough
                  for reader = (when (or (and (symbolp readerp) readerp)
                                         (smember field readerp))
                                 (find-attribute-reader field))
                  when reader
                  do
                    (loop
                        for result in results
                        for value = (get-field field result)
                        when (and reader value) do
                          (let ((foo (ignore-errors (funcall reader value))))
                            (when foo (setf (get-field field result) foo))))))
            ;;
            ;; _fix_me_
            ;; this is sort of hacky: since we fail to guarantee unique parse
            ;; ids, the corresponding run id would have to be included in the
            ;; `result' relation; as it stands, this is not the case |:-(.
            ;; until we get his fixed, it hard-wires the assumption that we
            ;; will not use the same profile to represent multiple test runs.
            ;;                                          (10-mar-99  -  oe)
            (unless sorted 
              (setf sorted 
                (sort (copy-list all) 
                      #'< :key #'(lambda (foo) (get-field :parse-id foo)))))
            (loop
                for item in sorted
                for key = (get-field :parse-id item)
                for matches =
                  (when (eql key (get-field :parse-id (first results)))
                    (loop
                        for result = (first results)
                        while (and result 
                                   (eql key (get-field :parse-id result)))
                        collect (pop results)))
                when matches
                do (nconc 
                    item 
                    (acons :results (sort 
                                     matches #'< 
                                     :key #'(lambda (foo)
                                              (get-field :result-id foo)))
                           nil))))
          (when trees
            (unless sorted 
              (setf sorted 
                (sort (copy-list all) 
                      #'< :key #'(lambda (foo) (get-field :parse-id foo)))))
            (loop
                for item in sorted
                for key = (get-field :parse-id item)
                for tree = (loop
                               with result = nil
                               for tree = (first trees)
                               for parse-id = (get-field :parse-id tree)
                               for version = (get-field :t-version tree)
                               while (eql parse-id key) do
                                 (pop trees)
                                 (when (or (null result)
                                           (> version 
                                              (get-field :t-version result)))
                                   (setf result tree))
                               finally (return result))
                when tree
                do (nconc item tree)))
          (when (or score gold)
            (unless sorted 
              (setf sorted 
                (sort (copy-list all) 
                      #'< :key #'(lambda (foo) (get-field :parse-id foo)))))
            (rank-items sorted :gold gold :score score :condition condition 
                        :sloppyp sloppyp :scorep scorep))
        
          (when filter
            (format
             *tsdb-io* "~%[~a] result-filter(): `~a' on <~{`~(~a~)'~^ ~}>:~%"
             (current-time :long :short) data *filter-test*)
            (setf result 
              (loop
                  with *tsdb-gc-message-p* = nil
                  for item in result
                  for foo = (funcall *statistics-result-filter* item)
                  when foo collect foo))
            (format
             *tsdb-io* "~%[~a] result-filter(): ~a item~p.~%~%"
             (current-time :long :short) (length result) (length result))))
        
        (setf (gethash key *tsdb-profile-cache*) result)))
    (when (smember purge '(:cache :all))
      (purge-profile-cache data :expiryp (eq purge :all)))
    (when (eq purge :db) (close-connections :data data))
    (when message (status :text (format nil "~a done" message) :duration 2))
    (when meter (meter :value (get-field :end meter)))
    result))