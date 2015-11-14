#include <stdio.h>
#include <sys/types.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>

void supprimer(char *phrase, char *recherche){
	char *suppr=strstr(phrase,recherche);
	suppr=suppr-1;
	*suppr='\0';
}

int main()
{
	struct dirent *Artist;
	DIR *rep;
	rep = opendir(".");

	FILE *file;
	file=fopen("insertArtist.sql","w+");
	fprintf(file, "INSERT INTO Artist(nomArtist) VALUES\n");


	while ((Artist = readdir(rep))) {
		if(Artist->d_type==DT_DIR && strcmp(Artist->d_name,".")!=0 && strcmp(Artist->d_name,"..")!=0 ){
            fprintf(file,"('%s'),\n",Artist->d_name);
		}
	}

	fclose(file);
	closedir(rep);
	return 0;
}


