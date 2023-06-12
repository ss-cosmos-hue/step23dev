#include <iostream>
#include <map>
#include <vector>
#include <fstream>
#include <sstream>
#include <algorithm>

class Wikipedia{
    public:
        std::string m_pages_file;
        std::string m_links_file;
        /*A mapping from a page ID (integer) to the page title.
        For example, self.titles[1234] returns the title of the page whose
        ID is 1234*/
        std::map<int,std::string> m_titles;
        /*A mapping from a page title to the page ID.
        */
        std::map<std::string,int> m_ids;
        /*A set of page links.
         For example, self.links[1234] returns an array of page IDs linked
         from the page whose ID is 1234.
        */
        std::map<int,std::vector<int> > m_links;
        Wikipedia(std::string pages_file,std::string links_file){
            m_pages_file = pages_file;
            m_links_file = links_file;
            // Read the pages file into titles.
            {
            std::ifstream input_file(pages_file);
            std::string line;
            if (!input_file.is_open()){
                std::cerr << "could not open the file " << pages_file << std::endl;
                return;
            }
            while(std::getline(input_file,line)){
                std::istringstream iss(line);
                std::string id_str, title;
                iss>>id_str>>title;
                int id = std::stoi(id_str);
                m_titles[id] = title;
                m_ids[title] = id;
                std::vector<int> links(0);
                m_links[id] = links;
            }
            input_file.close();
            std::cout<<"Finished reading" + pages_file<< std::endl;
            }
            {
            // Initialize the graph of pages.
            //Read the links file into links.
            std::ifstream input_file(links_file);
            std::string line;
            if (!input_file.is_open()){
                std::cerr << "could not open the file " << links_file << std::endl;
                return;
            }
            while(std::getline(input_file,line)){
                std::istringstream iss(line);
                std::string src_str, dst_str;
                iss>>src_str>>dst_str;
                int src = std::stoi(src_str);
                int dst = std::stoi(dst_str);
                m_links[src].push_back(dst);
            }
            input_file.close();

            std::cout<<"Finished reading" + links_file<< std::endl;
            }
            return;
        }
        void m_find_most_popular_pages(){
        std::map<int, int> id_to_list_idx;
        std::map<int, int> list_idx_to_id;
        int list_idx = 0;
        for (const auto& entry : m_titles) {
            int id = entry.first;
            id_to_list_idx[id] = list_idx;
            list_idx_to_id[list_idx] = id;
            list_idx++;
        }
        int N = m_titles.size();
        std::vector<double> page_rank(N, 1.0);
        int count = 0;
        while (true) {
            count++;
            if (count % 5 == 0) {
                std::cout << count << std::endl;
            }
            std::vector<double> new_page_rank(N, 0.15);
            double sum_deadend_page_rank = 0;
            for (int i = 0; i < N; i++) {
                int id = list_idx_to_id[i];
                const std::vector<int>& dsts = m_links[id];
                if (dsts.size() >= 1) {
                    double edge_val = 0.85 * page_rank[i] / dsts.size();
                    for (int dst : dsts) {
                        int dst_list_idx = id_to_list_idx[dst];
                        new_page_rank[dst_list_idx] += edge_val;
                    }
                } else {
                    sum_deadend_page_rank += page_rank[i];
                }
            }
            for (int i = 0; i < N; i++) {
                new_page_rank[i] += 0.85 * sum_deadend_page_rank / N;
            }

            double tolerance = 1e-2;
            double rank_sum_diff = 0;
            for (int i = 0; i < N; i++) {
                rank_sum_diff += (new_page_rank[i] - page_rank[i]);
            }
            assert(rank_sum_diff < tolerance);

            double convergence_threshold = 1e-2;
            bool updated = false;
            double sum_diff = 0;
            for (int i = 0; i < N; i++) {
                sum_diff += std::abs(page_rank[i] - new_page_rank[i]);
                if (sum_diff > convergence_threshold) {
                    updated = true;
                    page_rank = new_page_rank;
                    break;
                }
            }
            if (!updated) {
                break;
            }
        }

        int kNum = std::min(N, 3);
        std::vector<std::pair<double, int> > page_rank_listidx_tuples;
        for (int i = 0; i < N; i++) {
            page_rank_listidx_tuples.emplace_back(page_rank[i], i);
        }
        std::sort(page_rank_listidx_tuples.rbegin(), page_rank_listidx_tuples.rend());
        for (int i = 0; i < kNum; i++) {
            double rank = page_rank_listidx_tuples[i].first;
            int list_idx = page_rank_listidx_tuples[i].second;
            int id = list_idx_to_id[list_idx];
            std::cout << "page_rank: " << rank << ", id: " << id << ", title: " << m_titles[id] << std::endl;
        }
    }
};
                
int main(int argc,char* argv[]){
    Wikipedia wikipedia = Wikipedia(std::string(argv[1]), std::string(argv[2]));
    wikipedia.m_find_most_popular_pages();
    return EXIT_SUCCESS;
}
    