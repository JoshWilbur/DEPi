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
void Init_Screen(int thread_num, int h, int w){
    clear(); // Clear screen

    mvprintw((h/3)-5, (w/3), "Welcome to Conway's Game of Life!");
    mvprintw((h/3)-4, (w/3), "Thread count: %d", thread_num);
    mvprintw((h/3)-3, (w/3), "Board size: %d x %d", h, w);
    mvprintw((h/3)-2, (w/3), "Press 's' to start OR press 'e' to make board");
    mvprintw((h/3)-1, (w/3), "Press 'b' to benchmark");
    mvprintw((h/3), (w/3), "Press 'q' anytime to quit the game.");
    
    refresh(); // Apply changes
}