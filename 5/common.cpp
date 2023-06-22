#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>

class City
{
public:
    float x_, y_;
    City(float x, float y) : x_(x), y_(y){};
};

std::vector<City> read_input(const std::string &filename)
{
    std::vector<City> cities;
    std::ifstream file(filename);
    if (!file)
    {
        std::cerr << "Failed to open input file." << std::endl;
        return cities;
    }

    std::string line;
    std::getline(file, line); // Ignore the first line.

    while (std::getline(file, line))
    {
        std::istringstream iss(line);
        std::string xy;
        std::getline(iss, xy, ',');
        double x = std::stof(xy);
        std::getline(iss, xy, '\n');
        double y = std::stof(xy);
        cities.push_back(City(x, y));
    }
    file.close();
    return cities;
}
