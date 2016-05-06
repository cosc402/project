int magic(int b, int e) {
  int i;
  int result;
  result = 1;
  for (i=0; i<e; i+=1)
    result *= b;
  return result;
}

int main() {
  int i;
  _print(magic(2,10));
}
