#include "fair_distribution.h"

map <string, string> get_distribution(const map <string, int> &curr_score, const map <string, vector <string>> &solved, unsigned prob_limit)
{
	map <string, int> stud_id = get_id(curr_score);
	map <string, int> prob_id = get_id(solved);

	vector <string> stud_names = invert_map(stud_id);
	vector <string> prob_names = invert_map(prob_id);
	vector <int> prev_res = map_to_vector(curr_score);
	vector <vector <int> > options = get_options(solved, stud_id);

	vector <size_t> mask(options.size(), NOT_SOLVED), best_mask = mask;
	int max_solved = -1;
	double best_disp = INF;

	unsigned count = 0;
	do
	{
		vector <int> distribution = apply_mask(options, mask);
		int new_solved = tot_solved(distribution);
		if (new_solved < max_solved) continue;
		
		vector <int> test_score = count_score(distribution, stud_names.size());
		if (limit_exceeded(test_score, prob_limit)) continue;

		test_score = test_score + prev_res;

		double new_disp = count_disp(test_score);
		if (new_solved > max_solved || new_disp + EPS < best_disp)
		{
			max_solved = new_solved;
			best_disp = new_disp;
			best_mask = mask;
		}
	} while (advance_mask(mask, options));

	vector <int> best_distribution = apply_mask(options, best_mask);
	return translate_result(best_distribution, prob_names, stud_names);
}

static vector <string> invert_map(const map<string, int> &table)
{
	vector <string> answer(table.size());
	for (auto it = table.begin(); it != table.end(); it++)
	{
		answer[it->second] = it->first;
	}
	return answer;
}

static vector <int> apply_mask(const vector <vector <int>>& possible, const vector <size_t>& mask)
{
	vector <int> answer;
	for (unsigned prob = 0; prob < possible.size(); prob++)
	{
		if (mask[prob] == NOT_SOLVED)
		{
			answer.push_back(NOBODY);
			continue;
		}
		answer.push_back(possible[prob][mask[prob]]);
	}
	return answer;
}

static vector <vector<int>> get_options(const map<string, vector<string>>&solved, map <string, int>&stud_id)
{
	vector <vector <int>> answer(solved.size());
	int prob = 0;
	for (auto it = solved.begin(); it != solved.end(); it++, prob++)
	{
		size_t curr_size = it->second.size();
		for (size_t cand = 0; cand < curr_size; cand++)
		{
			answer[prob].push_back(stud_id[it->second[cand]]);
		}
	}
	return answer;
}

static vector<int> count_score(const vector<int> &students, unsigned size)
{
	vector <int> score(size, 0);
	for (unsigned i = 0; i < students.size(); i++)
	{
		if (students[i] == NOBODY) continue;
		score[students[i]]++;
	}
	return score;
}

static map<string, string> translate_result(const vector<int> &distribution, vector<string> &problems, vector<string> &students)
{
	map<string, string> answer;
	for (unsigned prob = 0; prob < distribution.size(); prob++)
	{
		if (distribution[prob] == NOBODY) continue;
		answer.insert(make_pair(problems[prob], students[distribution[prob]]));
	}
	return answer;
}

static vector<int> operator+(const vector<int> &a, const vector<int> &b)
{
	vector <int> answer(a.size());
	for (unsigned i = 0; i < answer.size(); i++)
	{
		answer[i] = a[i] + b[i];
	}
	return answer;
}

template<class first_T>
static vector<int> map_to_vector(const map<first_T, int> &table)
{
	vector <int> answer;
	for (auto it = table.begin(); it != table.end(); it++)
	{
		answer.push_back(it->second);
	}
	return answer;
}

template <class sec_T>
static map <string, int> get_id(const map <string, sec_T>& table)
{
	map <string, int> answer;
	int code = 0;
	for (auto it = table.begin(); it != table.end(); it++, code++)
	{
		answer.insert(make_pair(it->first, code));
	}
	return answer;
}

static double count_disp(const vector <int>& score)
{
	double avg = 0, disp = 0;
	unsigned size = score.size();

	for (auto it = score.begin(); it < score.end(); it++) avg += *it;
	avg /= size;

	for (auto it = score.begin(); it < score.end(); it++)
	{
		double delta = avg - *it;
		disp += delta * delta;
	}
	return sqrt(disp / size);
}

static bool limit_exceeded(const vector <int>& score, unsigned prob_limit)
{
	for (unsigned i = 0; i < score.size(); i++)
	{
		if (score[i] > (int)prob_limit) return true;
	}
	return false;
}

static int tot_solved(const vector<int> &students)
{
	int answer = students.size();
	for (unsigned pos = 0; pos < students.size(); pos++)
	{
		if (students[pos] == NOBODY) answer--;
	}
	return answer;
}

static bool advance_mask(vector <size_t>& mask, const vector <vector <int>>& masked_object)
{
	for (unsigned pos = 0; pos < masked_object.size(); pos++)
	{
		if (++mask[pos] < masked_object[pos].size()) return true;
		mask[pos] = NOT_SOLVED;
	}
	return false;
}