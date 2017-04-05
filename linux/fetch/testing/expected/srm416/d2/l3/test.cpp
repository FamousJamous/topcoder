#include "dancing_couples.h"
#include <cassert>
#include <iostream>
#include <string>
#include <vector>

namespace {

using namespace std;

void test(vector<string> canDance, int K, int exp) {
  int res = DancingCouples().countPairs(canDance, K);
  if (res != exp) {
    cerr << "exp " << exp << " res " << res << endl;
    assert(0);
  }
}

} // namespace

int main() {
  vector<string> canDance0 = {"YYYY", "YYYY", "YYYY"};
  int K0 = 3;
  int exp0 = 24;
  test(canDance0, K0, exp0);

  vector<string> canDance1 = {"YYNN", "NYYN", "NNYY"};
  int K1 = 3;
  int exp1 = 4;
  test(canDance1, K1, exp1);

  vector<string> canDance2 = {"YY", "YY", "YY"};
  int K2 = 3;
  int exp2 = 0;
  test(canDance2, K2, exp2);

  vector<string> canDance3 = {"YYNNNN", "NYYNNN", "NNYYNN", "NNNYYN", "NNNNYY", "YNNNNY"};
  int K3 = 3;
  int exp3 = 112;
  test(canDance3, K3, exp3);

  return 0;
}
