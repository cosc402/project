int main() {
    int i,j,k;
    i = 0;
    j = 1;
    k = 2;
    _print(i,j,k);

    if (k>i)
        _print("k > i");
    if (j>i)
        _print("j > i");
    if (i>j)
        _print("i > j");
    else
        _print("else works!");
}
