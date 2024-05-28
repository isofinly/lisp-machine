(progn 
    (read_char a)
    (while (> a 0)
      (progn
        (print_char a)
        (read_char a))))