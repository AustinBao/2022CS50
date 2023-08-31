#include "helpers.h"
#include <math.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // loops through every byte in the image
    for (int row = 0; row < height; row++)
    {
        for (int  col = 0; col < width; col++)
        {
            double average = (image[row][col].rgbtBlue + image[row][col].rgbtGreen + image[row][col].rgbtRed) / 3.0;

            // sets each bytes RGB to average colour
            image[row][col].rgbtRed = image[row][col].rgbtBlue = image[row][col].rgbtGreen = round(average);
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // loops through every byte in the image
    for (int row = 0; row < height; row++)
    {
        for (int  col = 0; col < width; col++)
        {
            // special sepia equations and variables
            double sepiaRed = (.393 * image[row][col].rgbtRed) + (.769 * image[row][col].rgbtGreen) + (.189 * image[row][col].rgbtBlue);
            double sepiaGreen = (.349 * image[row][col].rgbtRed) + (.686 * image[row][col].rgbtGreen) + (.168 * image[row][col].rgbtBlue);
            double sepiaBlue = (.272 * image[row][col].rgbtRed) + (.534 * image[row][col].rgbtGreen) + (.131 * image[row][col].rgbtBlue);

            // cases where sepia equation results in int greater than 255 (which RGB cant go over)
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }

            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }

            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            // set byte to each sepia colour
            image[row][col].rgbtRed = round(sepiaRed);
            image[row][col].rgbtGreen = round(sepiaGreen);
            image[row][col].rgbtBlue = round(sepiaBlue);
        }
    }
    return;

}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // gives me the end of the bytes index
    int end = width - 1;

    // loops through every byte in the image
    for (int y = 0; y < height; y++)
    {
        // REMEBER: width/2 is vital since it makes sure you arnt "undoing" your reflection by continuing past the middle.
        for (int x = 0; x < (width / 2); x++)
        {
            // simply just switches bytes from one side to the other
            RGBTRIPLE temp = image[y][x];
            image[y][x] = image[y][end - x];
            image[y][end - x] = temp;
        }
    }

    return;
}

// Blur image
// NEEDED TONS OF HELP
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // VITAL: creates extra image where we can place our new found blured bytes in order to not affect the results of other bytes
    RGBTRIPLE temp[height][width];

    // loops through every byte in the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // declare variables
            int total_Red = 0;
            int total_Blue = 0;
            int total_Green = 0;
            float counter = 0.00;

            // 3x3 box around current byte in which we need to caclulate the average RGB.
            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    int currentX = i + x;
                    int currentY = j + y;

                    // VITAL: checks if pointer / byte is outside of image
                    if (currentX < 0 || currentX > (height - 1) || currentY < 0 || currentY > (width - 1))
                    {
                        continue;
                    }

                    // update colours by adding it all to a collective sum
                    total_Red += image[currentX][currentY].rgbtRed;
                    total_Green += image[currentX][currentY].rgbtGreen;
                    total_Blue += image[currentX][currentY].rgbtBlue;

                    // number of bytes around your current byte which got added into your sum
                    counter++;
                }

                // sets each colours average to current byte
                temp[i][j].rgbtRed = round(total_Red / counter);
                temp[i][j].rgbtGreen = round(total_Green / counter);
                temp[i][j].rgbtBlue = round(total_Blue / counter);
            }
        }

    }

    // copies bytes from temp (where our blured bytes are all stored) into our ACTUAL image/output.
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
        }
    }
    return;
}
