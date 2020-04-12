#include "fair_distribution.h"

vector <string> split(string str, char c) {
	vector <string> res;

	int start = 0;
	for (int i = 0; i < str.size(); ++i) {
		if (str[i] == c) {
			res.push_back(str.substr(start, i - start));
			start = i + 1;
		}
	}
	res.push_back(str.substr(start, str.size() - start));

	return res;
}

void read_data(map <string, int>& points, map <string, vector <string>>& solved, char *Data) {
	string data(Data);

	size_t ind = data.find("#");
	string Points = data.substr(0, ind),
		   Solved = data.substr(ind + 1, data.size() - ind - 1);

	auto point_pairs = split(Points, ';'),
		solved_pairs = split(Solved, ';');

	for (auto i : point_pairs) {
		auto pair = split(i, ':');
		points[pair[0]] = stoi(pair[1]);
	}

	for (auto i : solved_pairs) {
		auto pair = split(i, ':');
		solved[pair[0]] = split(pair[1], ',');
	}
}

void write_data(const map <string, string>& distribution) {
	bool first = true;
	for (auto problem : distribution) {
		if (first)
			first = false;
		else
			cout << ";";

		cout << problem.first << ":" << problem.second;
	}
}

int main(int argc, char **argv) {
	map <string, int> points;
	map <string, vector<string>> solved;

	read_data(points, solved, argv[1]);

	map <string, string> distribution = get_distribution(points, solved, 2);

	write_data(distribution);

	return 0;
}