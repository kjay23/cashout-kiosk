
#define RELAY_PIN 8
#define COIN_SENSOR 2
#define MAX_COINS 4

int coinCount = 0;
bool systemLocked = false;
bool lastCoinState = HIGH;

unsigned long lastCoinTime = 0;
const unsigned long coinDebounceDelay = 50;

void setup() {
    Serial.begin(9600);
    pinMode(RELAY_PIN, OUTPUT);
    pinMode(COIN_SENSOR, INPUT_PULLUP);
    digitalWrite(RELAY_PIN, HIGH);
    Serial.println("System Ready. Dispensing started.");
}

void loop() {
    if (!systemLocked) {
        int coinState = digitalRead(COIN_SENSOR);
        if (lastCoinState == HIGH && coinState == LOW) {
            unsigned long currentTime = millis();
            if (currentTime - lastCoinTime > coinDebounceDelay) {
                coinCount++;
                lastCoinTime = currentTime;
                Serial.print("Coin Count: ");
                Serial.println(coinCount);
            }
        }
        if (coinState == HIGH) {
            lastCoinState = HIGH;
        } else {
            lastCoinState = LOW;
        }

        if (coinCount >= MAX_COINS) {
            Serial.println("Target reached. Stopping...");
            digitalWrite(RELAY_PIN, LOW);
            systemLocked = true;
        }
    }
}
