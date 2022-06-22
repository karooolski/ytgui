// Client side C/C++ program to demonstrate Socket
// programming
#include<iostream>
#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#define PORT 8080
#define IP "127.0.0.1"
using namespace std;

void show(char* XO) {

	for (int i = 0; i < 9; i++) {
		if (i % 3 == 0) cout << "\n\n";//<< "------"<<endl;
		cout << i << "\t";
	}
	cout << "\n\n";

	for (int i = 0; i < 9; i++) {
		if (i % 3 == 0) cout << "\n\n";//<< "------"<<endl;
		cout << (char)XO[i] << "\t";
	}
}

// bool ruch_nie_poprawny(char ruch){
// 	switch(ruch){
// 		case'0':{return false; break;}
// 		case'1':{return false; break;}
// 		case'2':{return false; break;}
// 		case'3':{return false; break;}
// 		case'4':{return false; break;}
// 		case'5':{return false; break;}
// 		case'6':{return false; break;}
// 		case'7':{return false; break;}
// 		case'8':{return false; break;}
// 		default:{
// 			cout <<"\n Ruch jest niepoprawny, oczekuje liczb od 0 do 8 \n";
// 			return true; break;} // prawda ruch jest niepoprawny == powtorz
// 	}
// }
 bool ruch_nie_poprawny(char *plansza , char moj_ruch){
	 int ruch = (int)moj_ruch-'0';
	 if(ruch>=0 && ruch <=8){
		 if (plansza[ruch]=='-'){
			return false; // ruch jest poprawny
		 }	
		else {cout <<"\nTo pole jest juz zajete!\n";return true;}
	 } 
	 else {cout <<"\n Ruch jest niepoprawny, oczekuje liczb od 0 do 8 \n";return true;}
	

 }


// bool pole_zajete(char *XO, char moj_ruch){
// 	int ruch = (int)moj_ruch-'0';
// 	if(ruch>=0 && ruch <=8){
// 		if(XO[ruch]=='-'){
// 			cout << "spoko pole nie jest zajete";
// 			return false; // pole nie jest zajete
// 		}
			
// 		else {
// 			cout <<"\nTo pole jest juz zajete!\n"; 
// 			return true;
// 		}
// 	}
// }

int connection(){ // logika Client <-> server
	 bool flag_f = true;
	 int first_animation = 0 ; 
	while(flag_f){
		int sock = 0, valread, client_fd;
		struct sockaddr_in serv_addr;
		char* hello = "Gracz: dzien dobry";
		char plansza[1024] = { 0 }; // wczesniej jako buffer
		char kim_jestem; // usuniecie kim_jestem[1] = {'i'}; spowodowalo ze nie mam dziwnch rzeczy na ekranie tylko same X/O 
		//<zabezpieczenia>-------------------------------------------------------------------------------
		if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
			printf("\n Socket creation error \n");
			return -1;
		}
		serv_addr.sin_family = AF_INET;
		serv_addr.sin_port = htons(PORT);
		// Convert IPv4 and IPv6 addresses from text to binary // form
		if (inet_pton(AF_INET, IP, &serv_addr.sin_addr) <= 0) { //10.3.10.182
			printf("\nInvalid address/ Address not supported \n");
			return -1;
		}
		if ((client_fd = connect(sock, (struct sockaddr*)&serv_addr,sizeof(serv_addr))) < 0) {
			printf("\nConnection Failed : Odpal serwer \n");
			return -1;
		}
		//</zabezpieczenia>------------------------------------------------------------------------------		
		bool flag = true;
		while(flag){ // moj while w sumie nic tu nie robi
			valread = read(sock,plansza, 1024); // zanim gracz odda ruch pierw zobaczy plansze
			kim_jestem = plansza[9];
			system("clear");
			show(plansza); // == printf("%s\n", plansza);
			char moj_ruch;
			cout <<"\n "<<kim_jestem<<" ";
			do{
				cin >> moj_ruch;
			}while(ruch_nie_poprawny(&plansza[0],moj_ruch));
			
			cout <<" wsyweitlam char " << moj_ruch << "\n";
			flag = false; // jak tu dasz true i usuniesz brake na dole do zyskasz 1 pusty ruch
			flag_f=false;
			send(sock, &moj_ruch, strlen(&moj_ruch), 0); // wysylam do serwera aktualny ruch
			valread = read(sock,plansza, 1024);
			break;
		}
	close(client_fd); // closing the connected socket
	}

}


int main(int argc, char const* argv[])
{
	
	connection();

	//cout << "wylaczenie:";
	//int notend; cin >> notend;
	return 0;
}
