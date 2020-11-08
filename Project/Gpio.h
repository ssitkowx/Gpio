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
        Gpio () = default;

        void SetPinLevel     (const uint16_t v_num, const bool v_state)    { derivedType.SetPinLevel     (v_num, v_state); }
        void SetPinDirection (const uint16_t v_num, const uint16_t v_mode) { derivedType.SetPinDirection (v_num, v_mode);  }
        bool ReadPinLevel    (const uint16_t v_num)                        { derivedType.ReadPinLevel    (v_num);          }
		
	private:
	    ~Gpio () = default;
};

///////////////////////////////////////////////////////////////////////////////
/////////////////////////////// END OF FILE ///////////////////////////////////
///////////////////////////////////////////////////////////////////////////////