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
	struct dirent *Music;
	DIR *rep;
	DIR *Dartist;
	DIR *Dalbum;
	rep = opendir(".");
	char route[300]=".";
	char routeImage[300]="/static/images/album";

	FILE *file;
	file=fopen("insertMusique.sql","w+");
	fprintf(file, "INSERT INTO Music(nomAlbum,titre,musicPath,caract) VALUES\n");


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
					Dalbum=opendir(route);

					while ((Music=readdir(Dalbum))){
						if (strstr(Music->d_name,".mp3")!=NULL){
							strcat(route,"/");
							strcat(route,Music->d_name);
							char titre[strlen(Music->d_name)];
							strcpy(titre,Music->d_name);
							titre[strlen(titre)-4]='\0';
							char caract[300];
							printf("Quelles sont les caractéristiques de cette musiques; %s - %s ?\n", Artist-> d_name ,Music->d_name);
							fgets(caract,300*sizeof(char) , stdin);
							caract[strlen(caract)-1]='\0';
							//printf("%s\n",caract);

							fprintf(file,"('%s','%s','/static/musiques/%s','%s'),\n",Album->d_name,titre,route+2, caract);
							//printf("%s\n",route);
							supprimer(route,Music->d_name);
						}
					}
					supprimer(routeImage,Album->d_name);
					supprimer(route,Album->d_name);
					closedir(Dalbum);
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
