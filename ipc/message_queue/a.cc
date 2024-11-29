#include <iostream>
#include <sys/msg.h>
#include <string>
#include <cstring>
#include <unistd.h>

struct message
{
    long mtype;
    char mtext[2];
};

// using cpp can achieve ~300k/s to ~500k/s throughput.
int main()
{
    // Create message queue
    key_t key = 12345; // Same key as used in Python example
    int msgid = msgget(key, IPC_CREAT | 0666);

    if (msgid == -1)
    {
        std::cerr << "Error creating message queue" << std::endl;
        return 1;
    }

    // Initialize message
    struct message msg;
    msg.mtype = 1; // Priority
    int counter = 0;

    // Continuously send messages
    while (true)
    {
        // Create message with counter
        snprintf(msg.mtext, sizeof(msg.mtext), "%d", counter);

        // Send message
        if (msgsnd(msgid, &msg, sizeof(msg.mtext), 0) == -1)
        {
            std::cerr << "Error sending message" << std::endl;
            break;
        }

        counter++;
        // if (counter > 10) {
        //     counter -= 10;
        // }
    }

    return 0;
}
