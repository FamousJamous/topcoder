#include "next_number.h"
#include <cassert>
#include <iostream>

namespace {

using namespace std;

void test(int N, int exp) {
  int res = NextNumber().getNextNumber(N);
  if (res != exp) {
    cerr << "exp " << exp << " res " << res << endl;
    assert(0);
  }
}

} // namespace

int main() {
  int N0 = 1717;
  int exp0 = 1718;
  test(N0, exp0);

  int N1 = 4;
  int exp1 = 8;
  test(N1, exp1);

  int N2 = 7;
  int exp2 = 11;
  test(N2, exp2);

  int N3 = 12;
  int exp3 = 17;
  test(N3, exp3);

  int N4 = 555555;
  int exp4 = 555557;
  test(N4, exp4);

  return 0;
}
