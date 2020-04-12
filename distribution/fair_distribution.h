#pragma once

#include <algorithm>
#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <map>

static const long long INF = 1e12;
static const long double EPS = 1e-6;

using namespace std;

enum
{
	NOT_SOLVED = (size_t)(-1),
	NOBODY = -1
};

map <string, string> get_distribution(const map <string, int>&, const map <string, vector <string>>&, unsigned);

template <class first_T>
static vector <int> map_to_vector(const map <first_T, int>&);

template <class sec_T>
static map <string, int> get_id(const map <string, sec_T>&);

static vector <string> invert_map(const map <string, int>&);
static vector <int> apply_mask(const vector <vector <int>>&, const vector <size_t>&);
static vector <vector <int>> get_options(const map <string, vector <string> >&, map <string, int>&);
static vector <int> count_score(const vector <int>&, unsigned);
static map <string, string> translate_result(const vector <int>&, vector <string>&, vector <string>&);
static bool limit_exceeded(const vector <int>&, unsigned);
static int tot_solved(const vector <int>&);

static bool advance_mask(vector <size_t>&, const vector <vector <int> >&);
static vector <int> operator + (const vector <int>&, const vector <int>& b);
static double count_disp(const vector <int>&);