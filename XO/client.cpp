// Client side C/C++ program to demonstrate Socket
// programming
#include<iostream>
#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#define PORT 8080
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
void show_z(){
		for (int i = 0; i < 9; i++) {
		if (i % 3 == 0) cout << "\n\n";//<< "------"<<endl;
		cout << '0' << "\t";
	}
}

int first_connection(){

		//return 10;
	//out << endl << endl;
	// logika Client - server
	bool flag_f = true;
	int first_animation = 0 ; 
	while(flag_f){
		int sock = 0, valread, client_fd;
		struct sockaddr_in serv_addr;
		char* hello = "Gracz: dzien dobry";
		char plansza[1024] = { 0 }; // wczesniej jako buffer
		char kim_jestem[1] = { 'i' };
//<zabezpieczenia>-------------------------------------------------------------------------------
		if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
			printf("\n Socket creation error \n");
			return -1;
		}
		serv_addr.sin_family = AF_INET;
		serv_addr.sin_port = htons(PORT);
		// Convert IPv4 and IPv6 addresses from text to binary // form
		if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) { //10.3.10.182
			printf("\nInvalid address/ Address not supported \n");
			return -1;
		}
		if ((client_fd = connect(sock, (struct sockaddr*)&serv_addr,sizeof(serv_addr))) < 0) {
			printf("\nConnection Failed \n");
			return -1;
		}
//</zabezpieczenia>------------------------------------------------------------------------------		
		bool flag = true;
		while(flag){ // moj while
			valread = read(sock,plansza, 1024); // zanim gracz odda ruch pierw zobaczy plansze
			kim_jestem[0] = plansza[9];
			//send(sock, &kim_jestem, strlen(&kim_jestem[0]), 0); // wysylam do serwera aktualny ruch
			//valread = read(sock,kim_jestem,1024); // oraz zobaczy czy napewno jest x czy y
			show(plansza); // == printf("%s\n", plansza);
			//send(sock, hello, strlen(hello), 0);
			//printf("Hello message from client sent to server\n");
			//valread = read(sock, plansza, 2024);
			
			//int a;
			//cin>>a;
			//char b = a + '0';
			char moj_ruch;
			cout <<"\n "<<kim_jestem<<" ";
			cin >> moj_ruch;
			cout <<" wsyweitlam char " << moj_ruch << "\n";
			flag = false; 
			flag_f=false;
			send(sock, &moj_ruch, strlen(&moj_ruch), 0); // wysylam do serwera aktualny ruch
			valread = read(sock,plansza, 1024);
			break;
		}
	// closing the connected socket
	close(client_fd);
	}

}


int main(int argc, char const* argv[])
{
	
	first_connection();

	cout << "wylaczenie:";
	int notend; cin >> notend;
	return 0;
}
