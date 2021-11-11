#include <iostream>
#include <string>
#include <map>
#include <unordered_map>
#include <vector>
#include <thread>
#include <sstream>
#include <iterator>
#include <fstream>
#include <ctime>
#include <iomanip>
#include <chrono>
#include <algorithm>
#include <mutex>
#include <deque>
#include <condition_variable>
#include <utility> 
#include "boost/thread/shared_mutex.hpp"
#include "boost/serialization/string.hpp"
#include "boost/algorithm/string/predicate.hpp"
#include "boost/algorithm/string/join.hpp"
#include "boost/lexical_cast.hpp"

#include "boost/archive/binary_oarchive.hpp"
#include "boost/archive/binary_iarchive.hpp"

#include "boost/serialization/vector.hpp"
#include "boost/serialization/map.hpp"


#include <boost/serialization/serialization.hpp>
#include <boost/serialization/unordered_map.hpp>
#include <boost/serialization/unordered_set.hpp>


/*
Author:     Emmanuel Salawu 
Email:      dr.emmanuel.salawu@gmail.com 


   Copyright 2016 Emmanuel Salawu

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


#Sample Compilation Commands
g++ load_db_and_listen_July21.cpp -o load_db_and_listen_July21.exe -std=c++11 -I/home/Emmanuel/boost_1_61_0 -L/home/Emmanuel/boost_1_61_0/stage/lib -lboost_serialization -lboost_thread -lboost_system -lpthread

g++ load_db_and_listen_July21.cpp -o load_db_and_listen_July21.exe -std=c++11 -I/usr/local/include/boost_1_61_0 -L/usr/local/include/boost_1_61_0/stage/lib -lboost_serialization -lboost_thread -lboost_system



g++ load_db_and_listen.cpp -o load_db_and_listen.exe -std=c++11 -I/home/Emmanuel/boost_1_61_0 -L/home/Emmanuel/boost_1_61_0/stage/lib -lboost_serialization -lboost_thread -lboost_system -lpthread

g++ load_db_and_listen.cpp -o load_db_and_listen.exe -std=c++11 -I/usr/local/include/boost_1_61_0 -L/usr/local/include/boost_1_61_0/stage/lib -lboost_serialization -lboost_thread -lboost_system

 */



std::unordered_map <std::string, std::vector <int> > the_indexes_for_file_alone;
int entries_per_db_seg = 100;
int number_of_jobs_left_to_be_fininshed;



boost::shared_mutex mutex_for_thread;
boost::shared_mutex mutex_for_thread_2;

std::condition_variable_any cond_any;
std::deque<std::function<void()> > work_queue;
bool priorityJobsStarted = false;
bool priorityJobsFinished = false;



class JoinThreads {
    std::vector<std::thread>& threads;
    public:
        explicit JoinThreads(std::vector<std::thread>& threads_):
        threads(threads_)
        {}
        ~JoinThreads() {
            for(unsigned long i=0;i<threads.size();++i) {
                if(threads[i].joinable())
                threads[i].join();
            }
        }
};

class ThreadPool {
    
    bool are_all_tasks_done;
    
    std::vector<std::thread> worker_threads;
    JoinThreads joiner;
    void worker_thread() {
        while (true) {
            std::function<void()> functor_of_task_to_be_done;
            //if (work_queue.size()) {
            		try {
		                if(mutex_for_thread.try_lock()){
		                	try {
		                		
		                		if (not (work_queue.size())) { 
		                			mutex_for_thread.unlock(); 
		                			std::this_thread::sleep_for (std::chrono::seconds(5));
		                			boost::this_thread::yield(); 
		                			continue; 
		                		}
		                		
				            	functor_of_task_to_be_done = work_queue.front();
				            	work_queue.pop_front();
				            } catch (...) {
			                }
		                	mutex_for_thread.unlock();
				        } else {
				            boost::this_thread::yield(); continue; //boost::this_thread::yield();
				        }
				    } catch (...) {
				    continue;
                    }
                    
                    try {
                        functor_of_task_to_be_done();
                        
                         //Decreament the number of jobs left to be fininshed
		                while (true) {
		                	if (mutex_for_thread_2.try_lock()) {
				            	if (number_of_jobs_left_to_be_fininshed > 0) {
				            		number_of_jobs_left_to_be_fininshed -= 1;
				            	}
				            	mutex_for_thread_2.unlock();
				            	break;
						    } else {
						        boost::this_thread::yield();//continue;
						    }
		                }
                    }
                    catch (...) {
                    }
                    
                   
                   
            /*}
            else {
                boost::this_thread::yield();
            }*/
        }
    }

    public:
        ThreadPool() 
        	:are_all_tasks_done(false), joiner(worker_threads) 
            {
                unsigned const n_threads_available =  (int) (std::thread::hardware_concurrency () - 4);
                try {
                    for (unsigned i=0; i<n_threads_available; ++i) {
                        worker_threads.push_back(std::thread(&ThreadPool::worker_thread,this));
                    }
                }
                catch (...) {
                    are_all_tasks_done=true;
                    throw;
                }
            }
        
        ///*
        void add_job(std::function<void()> f) {
            while (true) {
            	try {
		        	if (mutex_for_thread.try_lock()) {
		        		std::cout << "Adding job to queue ..." << std::endl;
		        		work_queue.push_back (std::function<void()> (f));
		        		mutex_for_thread.unlock();
		        		std::cout << "Job successfully added to queue" << std::endl;
		        		break;
		        	} else {
		        		boost::this_thread::yield();
		        	}
		        }
                catch (...) {
                }
            }
        }
        //*/
        
        /*
        void add_job(std::function<void()> f) {
            std::cout << "Adding job to queue ..." << std::endl;
            		work_queue.push_back (std::function<void()> (f));
            		std::cout << "Job successfully added to queue" << std::endl;
        }
        */
        int tasks_in_work_queue () {
        	return (int) work_queue.size();
        }
        
        ~ThreadPool() {
            are_all_tasks_done=true;
        }
};


void print_2 () {
    {
        cond_any.wait(mutex_for_thread,[]{return (priorityJobsStarted && work_queue.empty());});
        std::cout << 2 << std::endl;
    }
}



std::vector < std::vector <std::string> > read_fasta_file (std::string fasta_file_name) {
    
    std::ifstream opened_fast_a_file (fasta_file_name);
    
    std::vector <std::string> all_lines_in_file;
    
    for (std::string each_line; std::getline( opened_fast_a_file, each_line ); /**/ )
        all_lines_in_file.push_back( each_line );
    
    std::vector <std::vector <std::string> > fasta_sequences ;
    
    std::vector <std::string> each_fasta_entry; //{"header", "sequence"}
    int num_of_lines_in_file = all_lines_in_file.size ();
    std::vector <int> vector_of_fasta_start_positions;
    int line_num;
    for (line_num = 0; line_num < num_of_lines_in_file; line_num++) {
        //if (boost::starts_with (all_lines_in_file [line_num], ">") or boost::starts_with (all_lines_in_file [line_num], ";")) {
        if ((all_lines_in_file [line_num].find (">") == 0) or (all_lines_in_file [line_num].find (";") == 0)) {
                vector_of_fasta_start_positions.push_back (line_num);
            }
    }
    //Check the next line again for possible inclission //The next line is important because some sequences span more than one line in the fasta file 
    vector_of_fasta_start_positions.push_back (line_num);
    
    int num_of_fasta_seq = vector_of_fasta_start_positions.size ();
    std::string fasta_header;
    std::string residues_sequence;
    for (int index = 0; index < (num_of_fasta_seq - 1); index ++) {
        fasta_header = all_lines_in_file [vector_of_fasta_start_positions [index]];
        //Join many lines of sequences from fasta file 
        std::vector <std::string> sub_vector (all_lines_in_file.begin() + vector_of_fasta_start_positions [index] + 1, 
                    all_lines_in_file.begin() + vector_of_fasta_start_positions [index + 1]);
        residues_sequence = boost::algorithm::join (sub_vector, "");
        fasta_sequences.push_back (std::vector <std::string> {fasta_header, residues_sequence});
    }
    
    return fasta_sequences;
    
}



std::string check_waiting_jobs () {
    
    std::string file_name;
    
    return " " ;
}

std::vector<std::string> &split(const std::string &s, char delim, std::vector<std::string> &elems) {
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, delim)) {
        elems.push_back(item);
    }
    return elems;
}

std::vector <std::string> split_string (const std::string &s, char delim = '_') {
    std::vector<std::string> elems;
    split (s, delim, elems);
    return elems;
}



std::vector <std::vector <int> > combine_results_for_sub_queries_new ( std::vector <std::pair <std::vector <int> , std::string> > pre_values_from_database, std::vector <int> distances_between_start_positions ) {
    
    //std::cout << " A " << std::endl;
    
    std::unordered_map <std::string, std::vector <std::vector <int> > > this_database_seg;
    //std::cout << " B " << std::endl;
    std::vector <std::vector <int> > viable_results;
    std::vector <int> element1; //std::cout << " C " << std::endl;
    std::vector <int> element2; //std::cout << " D " << std::endl;
    std::vector <int> element3; //std::cout << " E " << std::endl;
    std::vector <std::vector <int> > first_vector; //std::cout << " F " << std::endl;
    std::vector <std::vector <int> > second_vector; //std::cout << " G " << std::endl;
    std::vector <std::vector <int> > third_vector; //std::cout << " H " << std::endl;
    //int size_first_vector; std::cout << " I " << std::endl;
    //int size_second_vector; std::cout << " J " << std::endl;
    //int size_third_vector; std::cout << " K " << std::endl;
    
    //std::vector <std::vector <std::vector <int> > > all_values_from_database; std::cout << " L " << std::endl;
    //std::vector <std::vector <int> > values_from_database; std::cout << " M " << std::endl;
    
    //std::pair <std::vector <int> , std::string> each_file_index_key_pair; std::cout << " N " << std::endl;
    
    std::vector <int> common_file_indexes; //std::cout << " O " << std::endl;
    std::vector <int> unique_dbfile_indexes; //std::cout << " P " << std::endl;
    //std::cout << pre_values_from_database.size() << std::endl;
    int levels_in_vector = (int) pre_values_from_database.size();
    
    //std::cout << "levels_in_vector " << levels_in_vector << std::endl;
    
    for ( int index1 = 0; index1 < pre_values_from_database [0].first.size (); index1++ ) {
    	//std::cout << index1 << std::endl;
    	if (levels_in_vector > 1) {
    		//std::cout << "pre_values_from_database [1].first.size() " << pre_values_from_database [1].first.size() << std::endl;
    		if (std::find ( std::begin (pre_values_from_database [1].first), std::end(pre_values_from_database [1].first), 
                 pre_values_from_database [0].first[index1] ) !=  std::end(pre_values_from_database [1].first)) {
                 if (levels_in_vector > 2) {
					if (std::find ( std::begin (pre_values_from_database [2].first), std::end(pre_values_from_database [2].first), 
			             pre_values_from_database [0].first[index1] ) !=  std::end(pre_values_from_database [2].first)) {
			             if (levels_in_vector > 3) {
							if (std::find ( std::begin (pre_values_from_database [3].first), std::end(pre_values_from_database [3].first), 
							     pre_values_from_database [0].first[index1] ) !=  std::end(pre_values_from_database [3].first)) {
							     //if 4
							     common_file_indexes.push_back (pre_values_from_database [0].first[index1]);
							}
						 }
						 else {
							//if 3
							//std::cout << index1 << std::endl;
							common_file_indexes.push_back (pre_values_from_database [0].first[index1]);
						}
			        }
			     }
		        else {
		        	//if 2
		        	//std::cout << index1 << std::endl;
		        	common_file_indexes.push_back (pre_values_from_database [0].first[index1]);
		        }
            }
    	}
    	else {
	    	//1
	    	//std::cout << index1 << std::endl;
	    	common_file_indexes.push_back (pre_values_from_database [0].first[index1]);
    	}
    }
    
    std::sort (common_file_indexes.begin(), common_file_indexes.end());
    
    int old_dbfile_index = -1;
    int new_dbfile_index = -1;
    for ( int index2 = 0; index2 < common_file_indexes.size (); index2++ ) {
    	new_dbfile_index = (int) common_file_indexes [index2] / entries_per_db_seg;
    	//std::cout << index2 << std::endl;
    	if ( new_dbfile_index != old_dbfile_index) {
    		//Load the file for new_dbfile_index
    		//this_database_seg = ;
    		
    		std::ifstream ifs_indexes_seg ("seg_dbs/indexes_seg_" + std::to_string (new_dbfile_index) + ".db");
			boost::archive::binary_iarchive ia_indexes_seg (ifs_indexes_seg);
			ia_indexes_seg >> this_database_seg;
    		
    		old_dbfile_index = new_dbfile_index;
    		
    	}
    	
    	for (std::vector <int> sub_values_from_database1 : this_database_seg [pre_values_from_database [0].second] ) {
			
			if (sub_values_from_database1[0] ==  common_file_indexes [index2]) {
				for ( int index3 = 1; index3 < sub_values_from_database1.size (); index3++ ) {
					if (levels_in_vector > 1) {
						for (std::vector <int> sub_values_from_database2 : this_database_seg [pre_values_from_database [1].second] ) {
							if ((common_file_indexes [index2] == sub_values_from_database2[0])
								and 
								(std::find ( std::begin (sub_values_from_database2) + 1, std::end(sub_values_from_database2), 
					            sub_values_from_database1 [index3] + distances_between_start_positions [0] ) !=  std::end(sub_values_from_database2))) {
								
								if (levels_in_vector > 2) {
									for (std::vector <int> sub_values_from_database3 : this_database_seg [pre_values_from_database [2].second] ) {
										if ((common_file_indexes [index2] == sub_values_from_database3[0])
											and 
											(std::find ( std::begin (sub_values_from_database3) + 1, std::end(sub_values_from_database3), 
											sub_values_from_database1 [index3] + distances_between_start_positions [0] + distances_between_start_positions [1] ) 
											!=  std::end(sub_values_from_database3))) {
											
											if (levels_in_vector > 3) {
												for (std::vector <int> sub_values_from_database4 : this_database_seg [pre_values_from_database [2].second] ) {
													if ((common_file_indexes [index2] == sub_values_from_database4[0])
														and 
														(std::find ( std::begin (sub_values_from_database4) + 1, std::end(sub_values_from_database4), 
														sub_values_from_database1 [index3] + distances_between_start_positions [0] 
														+ distances_between_start_positions [1] 
														+ distances_between_start_positions [2]) !=  std::end(sub_values_from_database4))) {
														
														// 4
														viable_results.push_back ( std::vector <int> {sub_values_from_database1 [0], sub_values_from_database1 [index3]} );
													}
												}
											}
											else {
												// 3
												viable_results.push_back ( std::vector <int> {sub_values_from_database1 [0], sub_values_from_database1 [index3]} );
											}
											
										}
									}
								}
								else {
									// 2
									viable_results.push_back ( std::vector <int> {sub_values_from_database1 [0], sub_values_from_database1 [index3]} );
								}
								
							}
						}
					}
					else {
						// 1
						viable_results.push_back ( std::vector <int> {sub_values_from_database1 [0], sub_values_from_database1 [index3]} );
					}
				}
			}
		}
		
	}
	
    return viable_results;
}



//std::vector <std::vector <int> > 
void process_each_query (std::string query_str, std::vector <std::vector <std::vector <int > > > &results, int pending_job_index_local, int num_pending_jobs_local) {
	
	std::cout << "pending_job_index_local: " << pending_job_index_local << std::endl;
	std::cout << "num_pending_jobs_local: " << num_pending_jobs_local << std::endl;
	
    std::vector <std::vector <int> > needed_results;
    std::vector <std::string> query_pieces = split_string (query_str);
    int query_pieces_size = query_pieces.size ();
    std::vector <std::pair < std::vector <int> , std::string> > values_from_database;
    std::pair < std::vector <int> , std::string> pair_file_index_and_key;
    std::vector <int> distances_between_start_positions;
    std::string key;
    
    for (int query_piece_index = 0; query_piece_index < query_pieces_size; query_piece_index++ ) {
    	std::cout << "query_pieces [query_piece_index] " << query_pieces [query_piece_index] << std::endl;
        if ((query_piece_index % 2) != 0 ) {
        	//std::cout << " Z " << std::endl;
	        distances_between_start_positions.push_back ( std::stoi (query_pieces [query_piece_index]) );
        }
        else {
        	//std::cout << " Y " << std::endl;
            key = query_pieces [query_piece_index];
            if ( the_indexes_for_file_alone.find (key) == the_indexes_for_file_alone.end() ) { //Key not in db
                //std::cout << "//results [pending_job_index_local] = needed_results;" << std::endl;
            }
            else {
            	//std::cout << " X " << std::endl;
                values_from_database.push_back ( std::make_pair (the_indexes_for_file_alone [key], key) );
            }
        }
    }
    //std::cout << "trying to combine results " << results.size() << std::endl;
    //std::cout << "values_from_database " << values_from_database.size() << std::endl;
    //std::cout << "distances_between_start_positions " << distances_between_start_positions.size() << std::endl;
    results [pending_job_index_local] =  combine_results_for_sub_queries_new ( values_from_database, distances_between_start_positions );
    //std::cout << query_str << " sample_results: " << results [pending_job_index_local].size () << ".\n" << std::flush;
    
    if (pending_job_index_local == (num_pending_jobs_local - 1)) {
    	std::this_thread::sleep_for (std::chrono::seconds(1));
    	priorityJobsFinished = true;
    }
}

ThreadPool thread_pool;


int main (int argc, char *argv[]) {

	unsigned int num_pending_jobs;
	unsigned int pending_job_index;
	unsigned int index_in_this_result;
	std::vector <int> allowed_spaces = {0, 1, 2, 3, 4};
	std::vector <std::vector <std::vector <int > > > results;
    
    //std::cout << argc << std::endl;
    
    std::string pending_jobs_file = "pending_jobs";
    std::vector < std::vector <std::string> > pending_jobs; 
    
    std::vector <std::string> entry_in_fastas;
    std::vector <std::string> a_pending_job;
    std::string a_pending_job_1;
    std::string needed_output = "";
    std::string file_name_pot_output;
    
    //ThreadPool thread_pool;
    
    std::vector < std::vector <std::string> > fasta_sequences;
    
    std::cout << "Loading FASTA sequences." << std::endl;
    
    std::ifstream ifs_fasta_sequences ("fasta_sequences.db");
    boost::archive::binary_iarchive ia_fasta_sequences (ifs_fasta_sequences);
    ia_fasta_sequences >> fasta_sequences;
    
    std::cout << "Done loading FASTA sequences. " << fasta_sequences.size() << std::endl;
    
    std::cout << "Loading Database and Indexes." << std::endl;
    
    std::ifstream ifs_indexes ("indexes.db");
    boost::archive::binary_iarchive ia_indexes (ifs_indexes);
    ia_indexes >> the_indexes_for_file_alone;
    
    std::cout << "Done loading Database and Indexes. " << the_indexes_for_file_alone.size() << std::endl;
    
    while (true) {
        
        std::cout << "Checking if there is any job to be done." << std::endl;
        
        pending_jobs = read_fasta_file (pending_jobs_file);
        
        
        num_pending_jobs = pending_jobs.size ();
        //number_of_jobs_left_to_be_fininshed = (int) num_pending_jobs;
        
        
        if ( num_pending_jobs > 0 ) {
        	
        	//ThreadPool thread_pool;
        	
        	while (true) {
            	if (mutex_for_thread_2.try_lock()) {
	            	number_of_jobs_left_to_be_fininshed = (int) num_pending_jobs;
	            	mutex_for_thread_2.unlock();
	            	break;
			    } else {
			        boost::this_thread::yield(); //continue;
			    }
            }
        	
		    std::ofstream new_empty_file (pending_jobs_file, std::ofstream::trunc);
		    //new_empty_file.open (pending_jobs_file);
		    new_empty_file << "";
		    new_empty_file.close();
            
            
            //std::vector <std::vector <std::vector <int > > > results (num_pending_jobs);
            results.resize (num_pending_jobs);
            
            std::cout << "Trying to do some work." << std::endl;
            priorityJobsFinished = false;
            
            /*std::time_t rawtime;
            struct tm * timeinfo;
            char buffer[80];
            std::time (&rawtime);
            timeinfo = std::localtime(&rawtime);

            std::strftime (buffer,80,"%d_%m_%Y_%H_%M_%S",timeinfo);
            */
            
            std::vector <std::string> output_file_name_from_fasta = split_string (pending_jobs [0][0], ' '); //[-1]
            //std::cout << output_file_name_from_fasta.back() << std::endl;
            std::string str(output_file_name_from_fasta.back());
            
            file_name_pot_output = str + ".output";
            
            
            for (pending_job_index = 0; pending_job_index < num_pending_jobs; pending_job_index++ ) {
                //a_pending_job = pending_jobs [pending_job_index];
                a_pending_job_1 = pending_jobs [pending_job_index] [1];
                
                //std::cout << a_pending_job_1 << std::endl;
                
               // thread_pool.add_job ([a_pending_job_1, &results, pending_job_index, num_pending_jobs] 
               // 	{process_each_query (a_pending_job_1, results, pending_job_index, num_pending_jobs);});
                
                thread_pool.add_job ([a_pending_job_1, &results, pending_job_index, num_pending_jobs] 
                	//()//(std::string a_pending_job_1, std::vector <std::vector <std::vector <int > > > & results, int pending_job_index, int num_pending_jobs) 
                	{process_each_query (a_pending_job_1, results, pending_job_index, num_pending_jobs);});
                
                //std::cout << a_pending_job_1 << " " <<  pending_job_index << " " << num_pending_jobs << std::endl;
            }
            
			priorityJobsStarted = true;
			//std::cout << " * " << std::endl;
			while (true) {
				//std::cout << " ** " << number_of_jobs_left_to_be_fininshed << std::endl;
				//if (not (thread_pool.tasks_in_work_queue ()) and priorityJobsFinished and (number_of_jobs_left_to_be_fininshed < 1)) {
				if (number_of_jobs_left_to_be_fininshed < 1) {
					std::this_thread::sleep_for (std::chrono::seconds( (int) (number_of_jobs_left_to_be_fininshed / 20) + 2));
					//work_queue.clear();
					break;
				}
				else {
				}
				std::this_thread::sleep_for (std::chrono::seconds( (int) (number_of_jobs_left_to_be_fininshed / 20) + 2));
            }
            //std::cout << " *** " << std::endl;
            for (pending_job_index = 0; pending_job_index < num_pending_jobs; pending_job_index++ ) {
                a_pending_job = pending_jobs [pending_job_index];
                //std::cout << " **** " << std::endl;
                if (results [pending_job_index].size () > 0) {
                    needed_output += ">" + a_pending_job [1] + "\n";
                    for (index_in_this_result = 0; index_in_this_result < results [pending_job_index].size (); index_in_this_result++ ) {
                        needed_output += fasta_sequences [results [pending_job_index][index_in_this_result][0]][0].substr (1) + " "
                        + fasta_sequences [results [pending_job_index][index_in_this_result][0]][1] + " "  
                        + std::to_string (results [pending_job_index][index_in_this_result][1]) + " " 
                        + std::to_string ( results [pending_job_index][index_in_this_result][0] ) + " "
                        + "\n";
                    }
                }
            }
            //std::cout << " ***** " << std::endl;
            std::ofstream myfile (file_name_pot_output, std::ofstream::trunc);
            
            myfile << needed_output;
            myfile.close();
            needed_output = "";
            results.clear();
            
        }
        std::cout << "Sleeping for 5 seconds." << std::endl;
        //work_queue.clear();
        std::this_thread::sleep_for (std::chrono::seconds(5));
    }
    
    return 0;
}

//
