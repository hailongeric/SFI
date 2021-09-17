

typedef unsigned long uint64_t;
typedef unsigned int  uint32_t;
typedef unsigned short uint16_t;
typedef unsigned char uint8_t;
typedef uint64_t u64;
typedef uint32_t u32;
typedef uint16_t u16;
typedef uint8_t u8;
typedef unsigned int size_t;

//#define sizeof(type) ((char *)(&type+1)-(char*)(&type))

static inline void sfi_memcpy(const void *dest, const void *src, size_t n)
{
    // Typecast src and dest addresses to (char *)
   char *csrc = (char *)src;
   char *cdest = (char *)dest;

    // Copy contents of src[] to dest[]
    for (int i=0; i<n; i++)
        cdest[i] = csrc[i];
}

static inline uint16_t sfi_ntohs(uint16_t const net) {
    uint8_t data[2] = {};
    sfi_memcpy(data, &net, sizeof(data));

    return (((uint16_t) data[1] << 0) | ((uint16_t) data[0] << 8));
}

static uint32_t sfimain()
{
    uint32_t crc = sfi_ntohs(70);

    return crc;
}

void foo(){}


void put_word(int* x){
    *x = 0x100;
}

url_loader_interface->Open(url_loader, request_info, callback_on_open);