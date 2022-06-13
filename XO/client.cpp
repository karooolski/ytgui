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

void show(char *XO){
	
	for(int i=0; i<9; i++){
		if(i%3==0) cout << "\n\n" ;//<< "------"<<endl;
		cout << i << "\t";
	}
	cout << "\n\n";

	for(int i=0; i<9; i++){
		if(i%3==0) cout << "\n\n" ;//<< "------"<<endl;
		cout << (char)XO[i] << "\t";
	}
}

bool no_winer(char *XO){
	for(int i = 0 ; i < 9 ; i++){
		if(XO[i]=='0')
			return false;
	}
	return true;
}

// 0 1 2 
// 3 4 5 
// 6 7 8 
// sprawdzanie kto wygral
bool check(char *XO){
	// poziomo gora
	if(XO[0]==XO[1] && XO[1]==XO[2]){
		if(XO[0]!='0'&&XO[1]!='0'&&XO[2]!='0'){
			show(&XO[0]);
			cout << "\n" << (char)XO[0] << " Winned the game(1)!";
			return true;
		}
	}
	// poziomo srodek
	if(XO[3]==XO[4] && XO[1]==XO[5]){
		if(XO[3]!='0'&&XO[4]!='0'&&XO[5]!='0'){
			show(&XO[0]);
			cout << "\n" << (char)XO[3] << " Winned the game!(2)";
			return true;
		}
	}
	// poziomo dol
	if(XO[6]==XO[7] && XO[7]==XO[8]){
		if(XO[6]!='0'&&XO[7]!='0'&&XO[8]!='0'){
			show(&XO[0]);
			cout << "\n" << (char)XO[6] << " Winned the game!(3)";
			return true;
		}
	}
	// skos od lewej 
	if(XO[0]==XO[4] && XO[4]==XO[8]){
		if(XO[0]!='0'&&XO[4]!='0'&&XO[8]!='0'){
			show(&XO[0]);
			cout << "\n" << (char)XO[0] << " Winned the game!(4)";
			return true;
		}
	}
	// skos od prawej
	if(XO[2]==XO[4] && XO[4]==XO[6]){
		if(XO[2]!='0'&&XO[4]!='0'&&XO[6]!='0'){
			show(&XO[0]);
			cout << "\n" << (char)XO[2] << " Winned the game!(5)";
			return true;
		}
	}
	// skos pion 1 
	if(XO[0]==XO[3] && XO[3]==XO[6]){
		if(XO[0]!='0'&&XO[3]!='0'&&XO[6]!='0'){
			show(&XO[0]);
			cout << "\n" << (char)XO[0] << " Winned the game!(6)";
			return true;
		}
	}
	// skos pion 2
	if(XO[1]==XO[4] && XO[4]==XO[7]){
		if(XO[1]!='0'&&XO[4]!='0'&&XO[7]!='0'){
			show(&XO[0]);
			cout << "\n" << (char)XO[1] << " Winned the game!(7)";
			return true;
		}
	}
			// skos pion 2
	if(XO[2]==XO[5] && XO[5]==XO[8]){
		if(XO[2]!='0'&&XO[5]!='0'&&XO[8]!='0'){
			show(&XO[0]);
			cout << "\n" << (char)XO[2] << " Winned the game!(8)";
			return true;
		}
	}
	if(no_winer(&XO[0])){
		show(&XO[0]);
		cout << "\n" << " No one winned the game!";
		return true;
	}
	return false;
}

char switcher(char player){
	if(player=='X') return 'Y';
	if(player=='Y') return 'X';
	else {cout << "\n switcher: blad!\n"; return 'S'; }
}

// sprawdzenie poprawnosci danych dla pojedynczych przypadkow
void check_test(){
	char XO[9];
	XO[0] = 'X'; XO[1] = '0'; XO[2] = '0';
	XO[3] = 'X'; XO[4] = '0'; XO[5] = '0';
	XO[6] = 'X'; XO[7] = '0'; XO[8] = '0';
	show(&XO[0]);
	check(&XO[0]);
	XO[0] = '0'; XO[1] = 'X'; XO[2] = '0';
	XO[3] = '0'; XO[4] = 'X'; XO[5] = '0';
	XO[6] = '0'; XO[7] = 'X'; XO[8] = '0';
	show(&XO[0]);
	check(&XO[0]);
	XO[0] = '0'; XO[1] = '0'; XO[2] = 'X';
	XO[3] = '0'; XO[4] = '0'; XO[5] = 'X';
	XO[6] = '0'; XO[7] = '0'; XO[8] = 'X';
	show(&XO[0]);
	check(&XO[0]);
	XO[0] = 'X'; XO[1] = '0'; XO[2] = '0';
	XO[3] = '0'; XO[4] = 'X'; XO[5] = '0';
	XO[6] = '0'; XO[7] = '0'; XO[8] = 'X';
	show(&XO[0]);
	check(&XO[0]);
	XO[0] = 'X'; XO[1] = 'Y'; XO[2] = 'Y';
	XO[3] = 'Y'; XO[4] = 'X'; XO[5] = 'X';
	XO[6] = 'X'; XO[7] = 'Y'; XO[8] = 'Y';
	show(&XO[0]);
	check(&XO[0]);
}


void game(){
	//check_test();
	//return 0;
	
	char XO[9];
	for(int i=0; i<9; i++)
	XO[i] = '0';
	XO[0] = '0'; XO[1] = '0'; XO[2] = '0';
	XO[3] = '0'; XO[4] = '0'; XO[5] = '0';
	XO[6] = '0'; XO[7] = '0'; XO[8] = '0';
	
	show(&XO[0]);

	char player;
	player = 'X';

	cout << endl;

	// logika gry
	while(!(check(&XO[0]))){ // dopoki nie ma wygranej albo /przegranej dla obu stron
		int wybierz_pole ; 
		bool stop = true;
		while(stop){ // dziala dopoki nie ustawisz pola
			show(&XO[0]);
			cout << player <<" "; cin >> wybierz_pole; // wybor pola
			if(wybierz_pole>-1 && wybierz_pole<9){
				if(XO[wybierz_pole]=='0'){
					XO[wybierz_pole] = player; // wpis pola
					cout << "ustawiono pole\n";
					player = switcher(player); // zamiana X na Y, Y na X
					stop = false;
				}else{
					cout << "\n to pole zostalo juz wybrane! \n";
				}
			}else{
				cout << "\n nieprawidlowe pole \n";
			}
		}
	}

}

int first_connection(){

		//return 10;
	//out << endl << endl;
	
	// logika Client - server
	while(true){
		int sock = 0, valread, client_fd;
		struct sockaddr_in serv_addr;
		char* hello = "Hello from client Madry";
		char buffer[1024] = { 0 };
		if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
			printf("\n Socket creation error \n");
			return -1;
		}

		serv_addr.sin_family = AF_INET;
		serv_addr.sin_port = htons(PORT);

		// Convert IPv4 and IPv6 addresses from text to binary
		// form
		if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) { //10.3.10.182
			printf("\nInvalid address/ Address not supported \n");
			return -1;
		}

		if ((client_fd = connect(sock, (struct sockaddr*)&serv_addr,sizeof(serv_addr))) < 0) {
			printf("\nConnection Failed \n");
			return -1;
		}

		while(true){ // moj while
			send(sock, hello, strlen(hello), 0);
			printf("Hello message from client sent to server\n");
			valread = read(sock, buffer, 1024);
			printf("%s\n", buffer);
			int a;
			cin>>a;
			char b = a + '0';
			char *y = &b;

			valread = read(sock,buffer, 1024);
			send(sock, y, strlen(y), 0);
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
