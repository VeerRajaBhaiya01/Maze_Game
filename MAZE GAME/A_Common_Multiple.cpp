#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <algorithm>
using namespace std;

int getMaxBeautifulSize(const vector<int>& a) {
    int n = a.size();
    map<int, int> freq;
    for (int val : a) freq[val]++;

    int maxSize = 0;

    // Try every possible product P from 1 to n * n
    for (int P = 1; P <= n * n; ++P) {
        set<int> used_y;
        int count = 0;

        for (auto& [x, f] : freq) {
            if (P % x != 0) continue;
            int y = P / x;

            // Make sure y is distinct
            if (used_y.count(y)) continue;

            used_y.insert(y);
            count += f;
        }

        maxSize = max(maxSize, count);
    }

    return maxSize;
}

int main() {
    int t;
    cin >> t;

    while (t--) {
        int n;
        cin >> n;
        vector<int> a(n);

        for (int i = 0; i < n; ++i) {
            cin >> a[i];
        }

        cout << getMaxBeautifulSize(a) << endl;
    }

    return 0;
}
