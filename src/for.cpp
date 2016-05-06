int global1;
int main() {
  int i;
  int j;
  for (i=0; i<10; i+=1) {
    j = i * 2;
    _print(j);
    _dump();
  }
}
