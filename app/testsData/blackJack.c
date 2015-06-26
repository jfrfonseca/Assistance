#include <stdio.h>
#include <stdlib.h>
#include <time.h>

//Matriz que verifica se a carta já foi retirada
int enable[4][13];

/*
 * cabecalho padrao
 */
void cabecalho()
{
    printf("Pontificia Universidade Catolica de Minas Gerais - PUC Minas\n");
    printf("Ciencia da Computacao\n");
    printf("Linguagens de Programacao - TP04\n");
    printf("Professor Marco\n");
    printf("Aluno: Douglas Henrique Silva Correa\tMatricula: 466503 \n");
    printf("Aluno: Wellington Santos Correa\t\tMatricula: 472047 \n\n");
}

/*
 * Enumeracao para o Naipe de cada Carta
 */
typedef enum Naipe
{
    Paus = 0,
    Copas,
    Espadas,
    Ouros,
}Naipe;

/*
 * Enumeracao para o Valor de cada Carta
 */
typedef enum Valor
{
    As = 1,
    Dois,
    Tres,
    Quatro,
    Cinco,
    Seis,
    Sete,
    Oito,
    Nove,
    Dez,
    Valete,
    Dama,
    Rei,
}Valor;

/*
 * Criando um tipo chamado Carta
 */
struct Carta
{
    Naipe naipe;
    Valor valor;
};
typedef struct Carta Card;

/*
 * Metodo para sortear uma carta
 */
Card sortear(  ){
    int tmp1, tmp2;
    Card sorteada;
    //Testa se a carta não foi sorteada
    do{
       tmp1 = (rand( ) % 13) + 1;
       tmp2 = rand( )%4;
    }while( enable[tmp2][tmp1 - 1] == 1 );
    enable[tmp2][tmp1 - 1] = 1;
    sorteada.valor = tmp1;
    sorteada.naipe = tmp2;
    return sorteada;
}

/*
 * Metodo para mostrar sua carta
 */
 void mostrarCarta( Card carta  ){
   char *valor = malloc( sizeof(char)*15);
   char *naipe = malloc( sizeof(char)*15);
   switch( carta.valor ){
        case 1: valor ="As";
        break;
        case 2: valor = "Dois";
        break;
        case 3: valor = "Tres";
        break;
        case 4: valor ="Quatro";
        break;
        case 5: valor ="Cinco";
        break;
        case 6: valor ="Seis";
        break;
        case 7: valor ="Sete";
        break;
        case 8: valor ="Oito";
        break;
        case 9: valor ="Nove";
        break;
        case 10: valor ="Dez";
        break;
        case 11: valor ="Valete";
        break;
        case 12: valor ="Dama";
        break;
        case 13: valor ="Rei";
        break;

   }
   switch( carta.naipe ){
       case 0: naipe = "Paus";
       break;
       case 1: naipe = "Copas";
       break;
       case 2: naipe = "Espadas";
       break;
       case 3: naipe = "Ouros";
       break;
   }
   printf("Foi retirada um(a) %s de %s!\n", valor, naipe);
   free(valor);
   free(naipe);
 }

 /*
 * Metodo que realiza o jogo de cartas 21
 */
   void jogar21( ){
   Card nova_carta;
   int rodada = 0;
   int aux;
   printf( "====================JOGO DE CARTAS 21===============================\n" );
   int opcao = 0;
   int quantidadeUser = 0, quantidadeCPU = 0;
   //Repetição para cada jogador tirar as 2 cartas iniciais
   for( aux = 0; aux < 4; aux++){
   if( aux < 2 ){
    printf( "\nComputador sacou uma carta.\n" );
    nova_carta = sortear( );
    mostrarCarta( nova_carta );
    if( nova_carta.valor > 10 ){

        quantidadeCPU += 10;
    }
    else{
        quantidadeCPU += nova_carta.valor;
    }
    printf( "Quantidade do Computador = %d\n", quantidadeCPU );
       }
       else{
            printf( "\nVoce sacou uma carta.\n" );
    nova_carta = sortear( );
    mostrarCarta( nova_carta );
    if( nova_carta.valor > 10 ){
        quantidadeUser += 10;
    }
    else{
        quantidadeUser += nova_carta.valor;
    }
    printf( "Sua Pontuacao = %d\n", quantidadeUser );
  }
  }
    system("pause");
    system("cls");
   //Continuacao jogo, o usuario escolhe uma opcao e prossegue o jogo
   while( ( quantidadeUser < 21 || opcao == 0 ) && quantidadeCPU < 21 ){
   if( rodada % 2 == 0 && quantidadeCPU < 21){
      printf( "\nRodada do Computador.\n" );
      printf( "Computador sacou uma carta.\n" );
      nova_carta = sortear( );
      mostrarCarta( nova_carta );
      if( nova_carta.valor > 10 ){
        quantidadeCPU += 10;
      }
      else{
         quantidadeCPU += nova_carta.valor;
      }
      printf( "Pontuacao do Computador = %d\n", quantidadeCPU );
  }
  else if ( rodada % 2 == 1 && opcao != 1 ){
    printf( "\nSua Rodada.\n" );
    printf( "\nVoce sacou uma carta.\n" );
    nova_carta = sortear( );
    mostrarCarta( nova_carta );
    if( nova_carta.valor > 10 ){

        quantidadeUser += 10;
    }
    else{
        quantidadeUser += nova_carta.valor;
    }
    printf( "Sua Pontuacao = %d\n", quantidadeUser );
    if( quantidadeUser < 21 ){
        printf( "Quer mais uma carta ?\n" );
        printf( "0 - Sim\n1 - Nao\n" );
        scanf( "%d", &opcao );
    }
    else{
        opcao = 1;
    }
    system("pause");
    system("cls");
  }
  rodada++;
  }
  //Anunciando se o Player ganhou ou perdeu
      if( quantidadeUser == 21 || quantidadeCPU > 21 ){
        printf( "\nParabens, voce venceu!\n" );
        opcao = 1;
    }
    else{
        printf( "\nQue pena, voce perdeu!\n" );
        opcao = 1;
    }
   }

int main( )
{
   cabecalho();
   srand ( time(NULL) );
   int i, j;
   //Inicializando cada posicao do Enable igual a 0
   for( i = 0; i < 4; i++ ){
    for( j = 0; j < 13; j++){
        enable[i][j] = 0;
    }
   }
   //Chamando o metodo para realizar o jogo
   jogar21( );
   return 0;
}
