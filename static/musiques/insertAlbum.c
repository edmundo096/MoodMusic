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
	struct dirent *Album;

	DIR *rep;
	DIR *Dartist;
	rep = opendir(".");
	char route[300]=".";
	char routeImage[300]="/static/images/album";

	FILE *file;
	file=fopen("insertAlbum.sql","w+");
	fprintf(file, "INSERT INTO Album(nomAlbum,nomArtist,Annee,Label,imagePath) VALUES\n");


	while ((Artist = readdir(rep))) {
		if(Artist->d_type==DT_DIR && strcmp(Artist->d_name,".")!=0 && strcmp(Artist->d_name,"..")!=0 ){
			strcat(route,"/");
			strcat(route,Artist->d_name);
			strcat(routeImage,"/");
			strcat(routeImage,Artist->d_name);
			Dartist=opendir(route);

			while ((Album = readdir(Dartist))){
				//printf("%s\n",route);
				if(Album->d_type==DT_DIR && strcmp(Album->d_name,".")!=0 && strcmp(Album->d_name,"..")!=0 ){
					strcat(route,"/");
					strcat(route,Album->d_name);
					strcat(routeImage,"/");
					strcat(routeImage,Album->d_name);
					strcat(routeImage,".jpg");

					char Annee[5];
                    printf("Quelles est l'année de cette album; %s - %s ?\n", Artist-> d_name ,Album->d_name);
                    fgets(Annee,6*sizeof(char) , stdin);
                    Annee[strlen(Annee)-1]='\0';

                    char Label[300];
                    printf("Quelles est le Label de cette album; %s - %s ?\n", Artist-> d_name ,Album->d_name);
                    fgets(Label,300*sizeof(char) , stdin);
                    Label[strlen(Label)-1]='\0';

                    fprintf(file,"('%s','%s',%s,'%s','%s'),\n",Album->d_name, Artist->d_name,Annee,Label,routeImage);

					supprimer(routeImage,Album->d_name);
					supprimer(route,Album->d_name);
				}
			}
			supprimer(routeImage,Artist->d_name);
			supprimer(route,Artist->d_name);
			closedir(Dartist);

		}
	}
	fclose(file);
	closedir(rep);
	return 0;
}

