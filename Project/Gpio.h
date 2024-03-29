#pragma once

///////////////////////////////////////////////////////////////////////////////
//////////////////////////////// INCLUDES /////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

#include <stdint.h>
#include <stdbool.h>

///////////////////////////////////////////////////////////////////////////////
/////////////////////////// CLASSES/STRUCTURES ////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

template <class DERIVED_TYPE>
class Gpio
{
    friend DERIVED_TYPE;
    DERIVED_TYPE & derivedType = static_cast <DERIVED_TYPE &> (*this);

    public:
        enum class EGpio : uint8_t
        {
            GpioA,
            GpioB,
            GpioC,
            GpioD
        };

        Gpio () = default;

        void SetGpio      (const EGpio vGpio)                      { derivedType.SetGpio             (vGpio);        }
        bool ReadPinLevel (const uint16_t vNum)                    { return derivedType.ReadPinLevel (vNum);         }
        void SetPinLevel  (const uint16_t vNum, const bool vState) { derivedType.SetPinLevel         (vNum, vState); }

    private:
        ~Gpio () = default;
};

///////////////////////////////////////////////////////////////////////////////
/////////////////////////////// END OF FILE ///////////////////////////////////
///////////////////////////////////////////////////////////////////////////////