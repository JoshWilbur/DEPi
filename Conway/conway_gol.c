#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <ncurses.h>

// Forward declarations
void Init_Board(int *board, int16_t h, int16_t w);
void Render(int *board, int16_t h, int16_t w);
int Handle_Input(int input);

// Arguments: thread count, board height
int main(int argc, char *argv[]){
    // Ncurses setup
    initscr();
    noecho();
    curs_set(0);
    nodelay(stdscr, TRUE); // Non-blocking key input

    printf("Welcome to Conway's Game of Life!\n");

    // Set up variables
    int16_t height = 50; 
    int16_t width = 25;
    int8_t thread_num = 1;

    // Handle thread argument if passed
    if (argv[1] != NULL){
        if ((atoi(argv[1]) < 8) && (atoi(argv[1]) >= 1)){
            thread_num = atoi(argv[1]);
        }
    }

    // Handle board size argument if passed
    if (argv[2] != NULL){
        if ((atoi(argv[2]) < 100) && (atoi(argv[2]) >= 10)){
            height = atoi(argv[2]);
            width = height / 2;
        }
    }

    printf("Starting game with %d x %d board size, press CTRL+C to stop\n", height, width);

    // Allocate mem for current and next board state
    int *board_c  = malloc(height * width * sizeof(int));
    int *board_n  = malloc(height * width * sizeof(int));
    Init_Board(board_c, height, width);

    // Infinite loop to run the game
    while(1){
        Render(board_c, height, width);
        usleep(100000); // Slow down game rendering

        if (Handle_Input(getch()) == 1) break; // Break if q is pressed
    }

    // Free memory for boards and ncurses
    free(board_c);
    free(board_n);
    endwin();
}

// Function to initialize the board with cells
void Init_Board(int *board, int16_t h, int16_t w){
    for (int y = 0;  y < h; y++){
        for (int x = 0; x < w; x++){
            board[y * w + x] = rand() % 2; // Generate random 0s and 1s
        }
    }
}

// Rendering the board using ncurses
void Render(int *board, int16_t h, int16_t w){
    clear(); // Clear screen

    for (int y = 0; y < h; y++) {
        for (int x = 0; x < w; x++) {
            mvprintw(y, x, board[y * w + x] ? "O" : " ");
        }
    }

    refresh(); // Apply changes
}

// Handle user input
int Handle_Input(int input){
    if (input == 'q') {
        return 1;
    }
    return 0;
}