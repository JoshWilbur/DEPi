// File to contain setup functions for Conway

// Function to initialize the board with cells
void Random_Board(int *board, int h, int w, int prob_alive){
    for (int y = 1;  y < h-1; y++){
        for (int x = 1; x < w-1; x++){
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
    mvprintw(11, 15, "Press 's' to start OR press 'e' to make board");
    mvprintw(13, 15, "Press 'q' anytime to quit the game.");
    
    refresh(); // Apply changes
}