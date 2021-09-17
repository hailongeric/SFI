#ifndef HEAD_H
#define HEAD_H

#define size_t unsigned long
#define u_int32_t unsigned int
#define u_char unsigned char
#define u_int16_t unsigned short

typedef unsigned long uint64_t;
typedef unsigned int uint32_t;
typedef unsigned short uint16_t;
typedef unsigned char uint8_t;

#ifdef DEBUG
#define LOG(_level_, _fmt_, ...)                   \
    do {                                           \
        fprintf(stderr,                            \
                "%c:%s: "_fmt_                     \
                "\n",                              \
                _level_, __func__, ##__VA_ARGS__); \
    } while (0)

#else
#define LOG(_level_, _fmt_, ...)
#endif /* LOGGER_H */

#define sizeof(type) ((char *)(&type+1)-(char*)(&type))


typedef uint64_t u64;
typedef uint32_t u32;
typedef uint16_t u16;
typedef uint8_t u8;

#define CTRL_ 0x00
#define CTRL_FD 1
#define CTRL_LRST 1 << 3  // reserved
#define CTRL_ASDE 1 << 5
#define CTRL_SLU 1 << 6
#define CTRL_ILOS 1 << 7  // reserved
#define CTRL_RST 1 << 26
#define CTRL_VME 1 << 30
#define CTRL_PHY_RST 1 << 31

#define STATUS 0x08

// Flow Control Address
#define FCAL 0x28
#define FCAH 0x2C
// Flow Control Type
#define FCT 0x30
// Flow Control Transmit Timer Value
#define FCTTV 0x170

// Interrupt Cause Read Regisetr
#define ICR 0xC0

// Interrupt Mask Set/Read Regisetr
#define IMS 0xD0
#define IMS_TXDW 1
#define IMS_TXQE 1 << 1
#define IMS_LSC 1 << 2
#define IMS_RXSEQ 1 << 3
#define IMS_RXDMT 1 << 4
#define IMS_RXO 1 << 6
#define IMS_RXT 1 << 7
#define IMS_RXQ0 1 << 20
#define IMS_RXQ1 1 << 21
#define IMS_TXQ0 1 << 22
#define IMS_TXQ1 1 << 23
#define IMS_OTHER 1 << 24

// Interrupt Mask Clear Register
#define IMC 0xD8

// Interrupt Vector Allocation Registers (for MSI-X)
#define IVAR 0x000E4
#define IVAR_RXQ0_VEC_SHIFT 0
#define IVAR_EN_RXQ0 1 << 3
#define IVAR_RXQ1_VEC_SHIFT 4
#define IVAR_EN_RXQ1 1 << 7
#define IVAR_TXQ0_VEC_SHIFT 8
#define IVAR_EN_TXQ0 1 << 11
#define IVAR_TXQ1_VEC_SHIFT 12
#define IVAR_EN_TXQ1 1 << 15
#define IVAR_OTHER_VEC_SHIFT 16
#define IVAR_EN_OTHER 1 << 19

// 3GIO Control Register
#define GCR 0x05B00

// Receive control
#define RCTL 0x100
#define RCTL_EN 1 << 1
#define RCTL_UPE 1 << 3
#define RCTL_MPE 1 << 4
#define RCTL_LPE 1 << 5
#define RCTL_LBM 1 << 6 | 1 << 7
#define RCTL_BAM 1 << 15
#define RCTL_BSIZE1 1 << 16
#define RCTL_BSIZE2 1 << 17
#define RCTL_BSEX 1 << 25
#define RCTL_SECRC 1 << 26

// Receive Descriptor Control
#define RXDCTL 0x02828

// Transmit Control
#define TCTL 0x400
#define TCTL_EN 1 << 1
#define TCTL_PSP 1 << 3

// Receive Descriptor Base Address
#define RDBAL 0x2800
#define RDBAH 0x2804
// Receive Descriptor Length
#define RDLEN 0x2808
#define RDH 0x2810
#define RDT 0x2818

// Transmit Descriptor Base Address
#define TDBAL 0x3800
#define TDBAH 0x3804
// Transmit Descriptor Length
#define TDLEN 0x3808
#define TDH 0x3810
#define TDT 0x3818

// Transmit Interrupt Delay Value
#define TIDV 0x3820

// Receive Address (MAC address)
#define RAL0 0x5400
#define RAH0 0x5404

// some statistics register
#define MPC 0x4010    // Missed Packets Count
#define GPRC 0x4074   // Good Packets Received Counts
#define GPTC 0x4080   // Good Packets Transmitted Count
#define GORCL 0x4088  // Good Octets Received Count
#define GORCH 0x408C
#define GOTCL 0x4088  // Good Octets Transmitted Count
#define GOTCH 0x408C
#define RXERRC 0x400C

// legacy descriptor
struct rdesc {
    u64 buffer;  // buffer address
    u16 length;
    u16 checksum;
    union {
        u8 status;
        struct {
            u8 dd : 1;     // descriptor done
            u8 eop : 1;    // end of packet
            u8 ixsm : 1;   //  ignore checksum indication
            u8 vp : 1;     // 802.1Q
            u8 udpcs : 1;  // UDP checksum calculated
            u8 tcpcs : 1;  // TCP checksum calculated
            u8 ipcs : 1;   // IPv4 checksum calculated
            u8 pif : 1;    // passed in-exact filter
        };
    };
    union {
        u8 error;
        struct {
            u8 ce : 1;    // CRC error
            u8 se : 1;    // symbol error
            u8 seq : 1;   // sequence error
            u8 rcv : 2;   // reserved
            u8 tcpe : 1;  // TCP/UDP checksum error
            u8 ipe : 1;   // IPv4 checksum error
            u8 rxe : 1;   // RX data error
        };
    };
    u16 vlantag;  // VLAN tag
} __attribute__((packed));

struct tdesc {
    u64 buffer;  // buffer address
    u16 length;
    u8 cso;  // checksum offset
    union {
        u8 command;
        struct {
            u8 eop : 1;   // end of packet
            u8 ifcs : 1;  // insert FCS
            u8 ic : 1;    // insert checksum
            u8 rs : 1;    // report status
            u8 rsv : 1;   // reserved
            u8 dext : 1;  // extension
            u8 vle : 1;   // VLAN packet enable
            u8 ide : 1;   // interrupt delay enable
        };
    };
    union {
        u8 status;
        struct {
            u8 dd : 1;    // descriptor done
            u8 ec : 1;    // excess collisions
            u8 lc : 1;    // late collisions
            u8 rsv2 : 5;  // reserved
        };
    };
    u8 css;       // checksum start
    u16 special;  // special field
} __attribute__((packed));


#define E1000_UDS_TYPE 2001
#define SFI_RX_INTR_CODE 0
#define SFI_TX_CODE 1
#define SFI_RX_CODE 2
#define HUGE_2M (2 * 1024 * 1024)
#define BUFSIZE 4096
#define PageSize 4096
#define NUM_OF_DESC 256  // 256 * 16 = 4096, 256* 4K = 1M, since we use 2M hugepage, don't make it to large;
#define PAGE_4K_ALIGN(size) (((size) & ~(PageSize-1)) + PageSize)  

#define HUGE_MAP_ADDRESS   (void*)0x48000000
#define HUGE_MAP_ADDRESS_2 (void*)0x49000000



#define E1000_ETHER_MINLEN 60
#define E1000_ETHER_MAXLEN 1514

#ifdef DEBUG
#define ASSERT(expr, msg, ...)                                             \
    do {                                                                   \
        if (!(expr)) {                                                     \
            fprintf(stderr, "[Error] %s:%3d %15s(): ", __FILE__, __LINE__, \
                    __func__);                                             \
            fprintf(stderr, msg "\n", ##__VA_ARGS__);                      \
            exit(1);                                                       \
        }                                                                  \
    } while (0)
#else
#define ASSERT(expr, msg, ...)     
#endif


struct e1000_user_buf {
    int send_head;
    int send_tail;
    int recv_head;
    int recv_tail;
    // sem_t  sem1;            /* POSIX unnamed semaphore */
    // sem_t  sem2;            /* POSIX unnamed semaphore */
    char send_ring[NUM_OF_DESC][BUFSIZE];
    char recv_ring[NUM_OF_DESC][BUFSIZE];
    u16 send_len[NUM_OF_DESC];
    u16 recv_len[NUM_OF_DESC];
    u32 rx_idx;
    uint8_t e1000_mac_buf[6];
}; 


#define LINK_MAC_ALEN 6

typedef uint8_t mac_addr_t[LINK_MAC_ALEN];

#define SFI_SUCESS 0x1000
#define SFI_SYSCALL_CODE 0x500
#define SFI_SYSCALL_CODE_STR "0x500"
#define SFI_LIBRARY_CALL_CODE 0x600 
#define SFI_LIBRARY_CALL_CODE_STR "0x600"
#define SFI_VOID_LIBRARY_FUNC -0x10

#define SFI_LIBRARY_GET_CALLEE_DRIVER_ID 0x601
#define SFI_LIBRARY_GET_SHARE_MEMORY 0x602
#define SFI_LIBRARY_GET_SHARE_DEV 0x603
#define SFI_LIBRARY_SHARE_MEMORY_ERROR -1
#define SFI_LIBRARY_WAIT_VALUE_TRUE_INTERRUPT 0x610
#define SFI_LIBRARY_WAIT_SUCCESS 0
#define SFI_LIBRARY_WAIT_ERROR -1
#define SFI_LIBRARY_WAKEUP_INTERRUPT 0x611
#define SFI_LIBRARY_WAIT_VALUE_TRUE_INTERRUPT_MEDDLESOME 0x612
#define SFI_LIBRARY_DEBUG_VOID 0x620
#define SFI_LIBRARY_DEBUG_VALUE 0x621
#define SFI_LIBRARY_ASSERT  0x622


#ifndef __GLOBL1
#define __GLOBL1(sym) __asm__(".globl " #sym)
#define __GLOBL(sym) __GLOBL1(sym)
#endif

#ifndef __used
#define __used __attribute__((__used__))
#endif

#ifndef __unused
#define __unused __attribute__((__unused__))
#endif

#ifndef __section
#define __section(x) __attribute__((__section__(x)))
#endif

#define __constructor __attribute__((constructor))
#define __destructor __attribute__((destructor))

/**
 * Returns a container of ptr, which is a element in some struct.
 * @param ptr       is a pointer to a element in struct.
 * @param type      is the type of the container struct.
 * @param member    is the name of the ptr in container struct.
 * @return Pointer to the container of ptr.
 */
#define container_of(ptr, type, member) \
    ((type *) ((uint8_t *) (ptr) -offsetof(type, member)))

#define num_elem(x) (sizeof(x) / sizeof(*(x)))

static inline int imax(int a, int b)
{
    return (a > b ? a : b);
}

static inline int imin(int a, int b)
{
    return (a < b ? a : b);
}

static inline long lmax(long a, long b)
{
    return (a > b ? a : b);
}

static inline long lmin(long a, long b)
{
    return (a < b ? a : b);
}

static inline unsigned int max(unsigned int a, unsigned int b)
{
    return (a > b ? a : b);
}

static inline unsigned int min(unsigned int a, unsigned int b)
{
    return (a < b ? a : b);
}

static inline unsigned long ulmax(unsigned long a, unsigned long b)
{
    return (a > b ? a : b);
}

static inline unsigned long ulmin(unsigned long a, unsigned long b)
{
    return (a < b ? a : b);
}

static inline unsigned int smin(size_t a, size_t b)
{
    return (a < b ? a : b);
}

static inline unsigned int uround_up(unsigned n, unsigned s)
{
    return ((n + s - 1) / s) * s;
}

#endif 