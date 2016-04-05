double m[6];

scale(double x) {
  int i;
  char c;

  c = 'a';
  
  if (x == 0)
    return 0;
  for (i = 0; i < 6; i += 1)
    m[i] *= x;
  return 1;
}
