#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <ncurses.h>

// Forward declarations
void Init_Board(int *board, int h, int w, int prob_alive);
void Init_Screen(int thread_num, int height, int width);
void Render(int *board, int h, int w);
void Apply_Rules(int *board_c, int *board_n, int h, int w);
int Check_Neighbors(int *board, int h, int w, int y, int x);


int main(int argc, char *argv[]){
    // Ncurses setup
    initscr();
    noecho(); // Prevent "echoing" of input to screen
    curs_set(0); // Don't show the mouse
    nodelay(stdscr, TRUE); // For non-blocking input

    // Set up variables
    int height = 50; 
    int width = 25;
    int thread_num = 1;
    long generation = 0;

    // If passed, handle arguments
    if (argc > 1){
        if (argv[1] != NULL && (atoi(argv[1]) < 8) && (atoi(argv[1]) >= 1)){
            thread_num = atoi(argv[1]);
        }
        if (argv[2] != NULL && (atoi(argv[2]) < 100) && (atoi(argv[2]) >= 10)){
            height = atoi(argv[2]);
            width = height / 2;
        }
    }

    // Show title screen
    Init_Screen(thread_num, height, width);

    // Allocate mem for current and next board state
    int *board_c  = malloc(height * width * sizeof(int));
    int *board_n  = malloc(height * width * sizeof(int));
    Init_Board(board_c, height, width, 10);


    // Infinite loop to run the game
    while(1){
        Render(board_c, height, width);
        generation++;
        Apply_Rules(board_c, board_n, height, width);
        usleep(1000000); // Slow down game rendering
        if (getch() == 'q') break; // Break if q is pressed
    }

    // Free memory for boards and ncurses
    free(board_c);
    free(board_n);
    endwin();
}

// Apply GOL rules to current board, output a new board
void Apply_Rules(int *board_c, int *board_n, int h, int w){
    int cell, live_n = 0;

    // Generate next board based on neighbors
    for (int y = 0; y < h; y++) {
        for (int x = 0; x < w; x++) {
            live_n = Check_Neighbors(board_c, h, w, y, x);
            cell = board_c[y * w + x]; // Current cell

            // Rule #1: If live cell has 1 or no neighbors = death by underpopulation
            // Rule #2: If live cell has 2 or 3 neighbors  = live
            // Rule #3: If live cell has over 3 neighbors  = death by overpopulation
            // Rule #4: If dead cell has 3 live neighbors  = birth

            if (cell == 1 && live_n > 2){ // Rule #1
                board_n[y * w + x] = 0;
            }else if (cell == 1 && (live_n == 2 || live_n == 3)){ // Rule #2
                board_n[y * w + x] = 1;
            }else if (cell == 1 && live_n > 3){ // Rule #3
                board_n[y * w + x] = 0;
            }else if (cell == 0 && live_n == 3){ // Rule #4
                board_n[y * w + x] = 0;
            }
        }
    }

    // Update current board for next round of processing
    for (int y = 0; y < h; y++) {
        for (int x = 0; x < w; x++) {
            board_c[y * w + x] = board_n[y * w + x];
        }
    }
}

// Render the board using ncurses
void Render(int *board, int h, int w){
    clear(); // Clear screen

    // Render board using a print statement
    for (int y = 0; y < h; y++) {
        for (int x = 0; x < w; x++) {
            mvprintw(y, x, board[y * w + x] ? "O" : " ");
        }
    }

    refresh(); // Apply changes
}

// Helper function to handle neighbor checking
int Check_Neighbors(int *board, int h, int w, int y, int x){
    int yn, xn, y_check, x_check, count = 0;

    // 8 possible neighbors according to game rules
    for (yn = -1; yn < 2; yn++){
        for (xn = -1; xn < 2; xn++){
            if (xn == 0 && yn == 0) continue; // Ignore current cell

            // Set point to check
            y_check = y + yn;
            x_check = x + xn;

            // Do a boundary check then increment (if neighbor)
            if (yn >= 0 && yn < h && xn >= 0 && xn < w){
                count += board[y_check * w + x_check];
            }
        }
    }
    return count; 
}

// Function to initialize the board with cells
void Init_Board(int *board, int h, int w, int prob_alive){
    for (int y = 0;  y < h; y++){
        for (int x = 0; x < w; x++){
            // Generate 1s and 0s to fill board
            if (rand() % 100 < prob_alive){ 
                board[y * w + x] = 1;
            }else{
                board[y * w + x] = 0;
            }
        }
    }
}

// Very simple title screen for the game
void Init_Screen(int thread_num, int height, int width){
    clear(); // Clear screen

    mvprintw(5, 15, "Welcome to Conway's Game of Life!");
    mvprintw(7, 15, "Thread count: %d", thread_num);
    mvprintw(9, 15, "Board size: %d x %d", height, width);
    mvprintw(11, 15, "Press 's' to start");
    mvprintw(13, 15, "Press 'q' anytime to quit the game.");
    
    refresh(); // Apply changes

    // If 's' is pressed, continue to the game
    while(1){
        if (getch() == 's') break;
    }
}