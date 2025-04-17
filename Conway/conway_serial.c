#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <ncurses.h>
#include <time.h>
#include <sys/time.h>

#include "setup.c"

#define DELAY_US 75000

// Forward declarations
void Render(int *board, int h, int w, int speed_us, int time_rules, int time_render, int time_loop, int stats_flag);
void Apply_Rules(int *board_c, int *board_n, int h, int w);
int Check_Neighbors(int *board, int h, int w, int y, int x);
void Set_Board(int *board, int height, int width);

// GLobal variables
long generation = 0;
int alive = 0;

int main(int argc, char *argv[]){
    // Declare variables
    int height = 40; 
    int width = 200;
    int thread_num = 1;
    int rules_time=0, render_time=0, loop_time=0;
    int edit_flag = 0;
    struct timeval start, end, loop_start, loop_end; // For wall-clock timing
    srand(time(NULL)); // Seed RNG

    // Ncurses setup (GNU recommends adding a void cast, unsure why)
    (void) initscr();
    (void) noecho(); 
    (void) curs_set(0); // Don't show the mouse
    (void) nodelay(stdscr, TRUE); // For non-blocking input

    // Auto-detect terminal size
    getmaxyx(stdscr, height, width);
    height -= 10;
    width -= 5;

    // If passed, handle arguments
    if (argc > 1){
        if (argv[1] != NULL && (atoi(argv[1]) < 8) && (atoi(argv[1]) >= 1)){
            thread_num = atoi(argv[1]);
        }
    }

    // Allocate mem for current and next board state
    int *board_c  = malloc(height * width * sizeof(int));
    int *board_n  = malloc(height * width * sizeof(int));

    // Show title screen and wait
    Init_Screen(thread_num, height, width);
    while(1){
        if (getch() == 's'){ // Continue with random board
            edit_flag = 0;
            break;
        }
        if (getch() == 'e'){ // Set board by hand
            edit_flag = 1;
            break;
        }
    }

    // Logic to handle board initialization
    if (edit_flag == 0) Random_Board(board_c, height, width, 10);
    else Set_Board(board_c, height, width);
    
    Render(board_c, height, width, DELAY_US, 0, 0, 0, 1);


    // Infinite loop to run the game
    while(1){
        gettimeofday(&loop_start, NULL);
        generation++;

        // Apply rules and measure time
        gettimeofday(&start, NULL);
        Apply_Rules(board_c, board_n, height, width);
        gettimeofday(&end, NULL);
        rules_time = end.tv_usec - start.tv_usec;

        // Render and measure time
        gettimeofday(&start, NULL);
        Render(board_n, height, width, DELAY_US, rules_time, render_time, loop_time, 1);
        gettimeofday(&end, NULL);
        render_time = end.tv_usec - start.tv_usec;

        // Pointer swap boards
        int *temp_board = board_c;
        board_c = board_n;
        board_n = temp_board;

        // Handle user input
        if (getch() == 'q') break; // Break if q is pressed

        gettimeofday(&loop_end, NULL);
        loop_time = loop_end.tv_usec - loop_start.tv_usec;
        usleep(DELAY_US);
    }

    // Free memory for boards and ncurses
    free(board_c);
    free(board_n);
    (void) endwin();
    return 0;
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

            if (cell == 1) {
                if (live_n < 2 || live_n > 3) board_n[y * w + x] = 0;  // Rule 1
                else board_n[y * w + x] = 1; // Rule 2
            } else {
                if (live_n == 3) board_n[y * w + x] = 1;  // Rule 3
                else board_n[y * w + x] = 0; //  Rule 4
            }
        }
    }
}

// Render the board using ncurses
void Render(int *board, int h, int w, int speed_us, int time_rules, int time_render, int time_loop, int stats_flag){
    clear(); // Clear screen
    alive = 0;

    // Draw top and bottom borders
    for (int x = 0; x < w+2; x++) {
        mvprintw(0, x, "-");
        mvprintw(h+1, x, "-");
    }

    // Draw left and right borders
    for (int y = 0; y < h+2; y++) {
        mvprintw(y, 0, "|");
        mvprintw(y, w+1, "|");
    }

    // Render board using a print statement
    for (int y = 0; y < h; y++) {
        for (int x = 0; x < w; x++) {
            // Render cells, offset by 1 for borders
            mvprintw(y+1, x+1, board[y * w + x] ? "0" : " ");
            if (board[y * w + x] == 1) alive++;
        }
    }

    if (stats_flag){
        float speed_ms = speed_us / 1000;
        mvprintw(h+2, (w/3), "Generation: %ld | Population: %d | Speed: %.1fms | Press 'q' to quit.", generation, alive, speed_ms);
        mvprintw(h+3, (w/3), "Rule time: %dus | Render time: %dus | Loop time: %dus", time_rules, time_render, time_loop);
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
            if (y_check >= 0 && y_check < h && x_check >= 0 && x_check < w){
                count += board[y_check * w + x_check];
            }
        }
    }
    return count; 
}

// Function to manually set an initial board
void Set_Board(int *board, int h, int w){
    // Start with an empty board
    int x,y;
    for (y = 1;  y < h-1; y++){
        for (x = 1; x < w-1; x++){
            board[y * w + x] = 0;
        }
    }
    
    // Render board without stats
    Render(board, h, w, DELAY_US, 0, 0, 0, 0);
    mvprintw(h+2, (w/2), "EDIT MODE");
    mvprintw(h+3, (w/3), "Press 'c' to begin the game. Use WASD to navigate the board");
    mvprintw(h+4, (w/3), "Press the spacebar to toggle a cell");

    // Reset index variables before constructing board
    x = w/2;
    y = h/2;
    while(1){
        // Switch case for user input
        switch(getch()){
            case 'c': // Continue to game if c is pressed
                return;
            case 'w': // Move up
                if (y > 1) y--;
                break;
            case 's': // Move down
                if (y < h-1) y++;
                break;
            case 'a': // Move left
                if (x > 1) x--;
                break;
            case 'd': // Move left
                if (x < w-1) x++;
                break;
            case ' ': // Toggle cell
                board[y * w + x] ^= 1;
                if (board[y * w + x]) mvprintw(y+1, x+1, "0");
                else mvprintw(y+1, x+1, " ");
                refresh();
                break;
            default:
                break;
        }

        if (!(board[y * w + x])){
            mvprintw(y+1, x+1, "#");
            refresh();
            usleep(10000);
            mvprintw(y+1, x+1, " ");
        }
        refresh(); // Update screen
    }
}