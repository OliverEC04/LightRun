#include <FastLED.h> 

#define STRIP1_PIN 7
#define STRIP2_PIN 8
#define STRIP3_PIN 2
#define STRIP4_PIN 3
#define STRIP5_PIN 4
#define STRIP_NUM 30
#define BTN_PIN 6
#define LED_PIN 5
#define BUZZ_PIN 16
#define P0_PIN 0
#define P1_PIN 1
#define SPEED 5

int tick = 0;
int hitTick = 0;
bool btnBegin = false;
bool foot = false;
int score = 0;

CRGB strips[5][STRIP_NUM];

uint8_t track[5][60] = {
  {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
  {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
  {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0},
  {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
  {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
};

void drawTrack0()
{
  for (int y = 0; y < 60; y++)
  {
    for (int x = 0; x < 5; x++)
    {
      track[x][y] = 0;
    }
  }

  track[2][58] = 1;
}

void drawTrack1()
{
  for (int y = 0; y < 60; y++)
  {
    for (int x = 0; x < 5; x++)
    {
      track[x][y] = 5;
    }
  }

  track[2][58] = 1;
}

void drawTrack2()
{
  uint8_t trackNew[5][30] = {
    {0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0}
  };

  for (int y = 0; y < 30; y++)
  {
    for (int x = 0; x < 5; x++)
    {
      track[x][y] = trackNew[x][y];
    }
  }
}

void drawTrack3()
{
  uint8_t trackNew[5][30] = {
    {0, 0, 0, 0, 0, 0, 2, 3, 2, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0},
    {2, 2, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 2, 3, 2, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
  };

  for (int y = 0; y < 30; y++)
  {
    for (int x = 0; x < 5; x++)
    {
      track[x][y] = trackNew[x][y];
    }
  }
}

CRGB convert (const int& value)
{
  switch(value)
  {
    case 0:
      return CRGB(0, 0, 0); // Empty
    case 1:
      return CRGB(255, 255, 255); // Player
    case 2:
      return CRGB(100, 0, 0); // Barrier Bar
    case 3:
      return CRGB(0, 100, 0); // Hole
    case 4:
      return CRGB(255, 0, 255); // Hit thing
    case 5:
      return CRGB(100, 30, 0); // Game stopped
  }
}

void setup()
{
  Serial.begin(9600);
  pinMode(BTN_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  Serial.println("begin");
  
  FastLED.addLeds<WS2812, STRIP1_PIN, GRB>(strips[0], STRIP_NUM);
  FastLED.addLeds<WS2812, STRIP2_PIN, GRB>(strips[1], STRIP_NUM);
  FastLED.addLeds<WS2812, STRIP3_PIN, GRB>(strips[2], STRIP_NUM);
  FastLED.addLeds<WS2812, STRIP4_PIN, GRB>(strips[3], STRIP_NUM);
  FastLED.addLeds<WS2812, STRIP5_PIN, GRB>(strips[4], STRIP_NUM);

  drawTrack3();
  drawTrack1();
}

void loop()
{ 
  tick++; //TODO: score
  Serial.println(digitalRead(BTN_PIN));
  Serial.println("P0");
  Serial.println(analogRead(P0_PIN));
  Serial.println("P1");
  Serial.println(analogRead(P1_PIN));

  if (digitalRead(BTN_PIN) == 1)
  {
    btnBegin = true;
    digitalWrite(LED_PIN, LOW);
  }

  for (int y = 59; y >= 0; y--)
  {
    for (int x = 0; x < 5; x++)
    {
      if (track[x][y] == 1)
      {
        if (analogRead(P0_PIN) > 500 && analogRead(P1_PIN) < 500 && foot == false)
        {
          foot = true;
          track[x][y] = 0;
          track[x <= 0 ? 0 : x - 1][y] = 1;
          Serial.println("right");
        }
        
        if (analogRead(P1_PIN) > 500 && analogRead(P0_PIN) < 500 && foot == false)
        {
          foot = true;
          track[x][y] = 0;
          track[x >= 4 ? 4 : x + 1][y] = 1;
          Serial.println("left");
        }

        if (analogRead(P1_PIN) < 500 && analogRead(P0_PIN) < 500)
        {
          foot = false;
        }
        
        /*
        BEVÆGELSE KODE TIL GAMMEL MÅDE
        if (analogRead(P0_PIN) > 500 && analogRead(P1_PIN) < 100) // Left
        {
          track[x][y] = 0;
          track[4][58] = 1;
        }
        if (analogRead(P0_PIN) < 500 && analogRead(P0_PIN) > 100 && analogRead(P1_PIN) < 100) // mid-left
        {
          track[x][y] = 0;
          track[3][58] = 1;
        }
        if (analogRead(P0_PIN) < 100 && analogRead(P1_PIN) < 100) // Middle
        {
          track[x][y] = 0;
          track[2][58] = 1;
        }
        if (analogRead(P0_PIN) < 100 && analogRead(P1_PIN) < 500 && analogRead(P0_PIN) > 100) // mid-right
        {
          track[x][y] = 0;
          track[1][58] = 1;
        }
        if (analogRead(P0_PIN) < 100 && analogRead(P1_PIN) > 500) // right
        {
          track[x][y] = 0;
          track[0][58] = 1;
        }
        */

        if (track[x][y - 1] == 2 || (track[x][y - 1] == 3 && analogRead(P0_PIN) < 500 && analogRead(P1_PIN) < 500)) // Collision
        {
          hitTick = tick;
          Serial.println("hit");
          btnBegin = false;
          drawTrack1();
          score = 0;
          digitalWrite(BUZZ_PIN, HIGH);
        }
      }
      
      if (track[x][y] != 1 && track[x][y - 1] != 1 && tick % SPEED == 0) // Move track down
      {
        track[x][y] = y == 0 ? 0 : track[x][y - 1];
      }
    }
  }

  for (int i = 0; i < STRIP_NUM; i++)
  {
    strips[0][i] = convert(track[0][i + STRIP_NUM]);
    strips[1][i] = convert(track[1][i + STRIP_NUM]);
    strips[2][i] = convert(track[2][i + STRIP_NUM]);
    strips[3][i] = convert(track[3][i + STRIP_NUM]);
    strips[4][i] = convert(track[4][i + STRIP_NUM]);
  }

  if (tick > hitTick + 2)
  {
    digitalWrite(BUZZ_PIN, LOW);
  }

  if (btnBegin)
  {
    if (tick % (30 * SPEED) == 0)
    {
      switch (random(2, 4))
      {
        case 2:
          drawTrack2();
          break;

        case 3:
          drawTrack3();
          break;
      }
      
      score++;
      Serial.print("score");
      Serial.println(score);
    }

    for (int i = 0; i < score; i++)
    {
      if (i < 5)
      {
        strips[i % 5][30] = CRGB(0, 0, 255);
      }
      if (i >= 5 && i < 10)
      {
        strips[i % 5][31] = CRGB(0, 0, 255);
      }
    }
  }
  else
  {
    if (tick % 10 < 5)
    {
      digitalWrite(LED_PIN, HIGH);
    }
    else
    {
      digitalWrite(LED_PIN, LOW);
    }
    
    if (tick % (30 * SPEED) == 0)
    {
      drawTrack1();
    }
  }

  FastLED.show();
  delay(50);
  
}