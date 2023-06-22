#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>

#include "common.h"
#include "solve_2opt.h"

std::string format_tour(const std::vector<int> &tour)
{
    std::ostringstream oss;
    oss << "index" << std::endl;
    for (int city_id : tour)
    {
        oss << city_id << std::endl;
    }
    return oss.str();
}

void generate_output(const int CHALLENGES)
{
    for (int i = 3; i < CHALLENGES; i++)

    {
        std::cout << i << std::endl;

        std::string input_filename = "input_" + std::to_string(i) + ".csv"; // 入力ファイル名を生成
        std::vector<City> cities = read_input(input_filename);
        std::cout << "input has been read" << std::endl;

        // 2optによる解法処理
        std::vector<int> tour = solve_two_opt(cities);

        std::string output_filename = "output_" + std::to_string(i) + ".csv"; // 出力ファイル名を生成
        std::ofstream output_file(output_filename);
        if (!output_file)
        {
            std::cerr << "Failed to open output file: " << output_filename << std::endl;
            continue;
        }
        output_file << format_tour(tour);
        output_file.close();
    }
}

int main()
{
    generate_output(4);
    return EXIT_SUCCESS;
}
