(progn
  (include "functions/io.lisp")

  (setq a 0)
  (setq b 1)
  (setq sum 0)

  (while (< b 4000000)
      (progn
          (if 
              (= (% b 2) 0)
              (setq sum (+ sum b))
          (0))
          (setq a b)
          (setq b (+ a b))
      ))

  (print_int sum)
  )