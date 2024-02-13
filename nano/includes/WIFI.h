#if !defined(_WIFI_H)
#define _WIFI_H

#include <WiFi.h>
#include <esp_wifi.h>
#include <stdint.h>

typedef wificonfig_t wifi_t;

class WIFI_ESP
{
private:
    wifi_t wifi;
public:
    WIFI_ESP(/* args */);
    ~WIFI_ESP();
};

WIFI_ESP::WIFI_ESP(/* args */)
{
}

WIFI_ESP::~WIFI_ESP()
{
}


#endif // WIFI header guard
