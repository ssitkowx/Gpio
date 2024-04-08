#pragma once 

///////////////////////////////////////////////////////////////////////////////
//////////////////////////////// INCLUDES /////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

#include "Gpio.h"
#include "gmock/gmock.h"

///////////////////////////////////////////////////////////////////////////////
/////////////////////////// CLASSES/STRUCTURES ////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

class GpioHw final : public Gpio <GpioHw>
{
    public:
        GpioHw () = default;
        ~GpioHw () = default;

        MOCK_METHOD1 (SetGpio     , void (const EGpio));
        MOCK_METHOD1 (ReadPinLevel, bool (const uint16_t));
        MOCK_METHOD2 (SetPinLevel , void (const uint16_t, const bool));
};

///////////////////////////////////////////////////////////////////////////////
/////////////////////////////// END OF FILE ///////////////////////////////////
///////////////////////////////////////////////////////////////////////////////