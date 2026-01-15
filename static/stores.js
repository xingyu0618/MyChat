import {RecentChatList} from "./recentChatList";
import {deleteDB, getChatsFromDB, getFriendsFromDB, putChatsToDB, putFriendsToDB} from "./db";
import Alpine from "alpinejs";

function getJsonScriptData(id) {
    const element = document.getElementById(id)
    if (!element) {
        return null
    }
    return JSON.parse(element.textContent)
}

async function loadFull() {
    await deleteDB()

    const friends = getJsonScriptData('friends') ?? []
    const states = getJsonScriptData('states') ?? []

    friendStore.setFriends(friends)
    chatStore.rebuildFrom(states)

    await putFriendsToDB(friends)
    await putChatsToDB(states)
}

function setupChatStore() {
    const chatStoreName = 'chats'
    Alpine.store(chatStoreName, {
        manager: null,
        conversations: [],
        totalUnread: null,
        init() {
            console.log("[*] chatStore初始化")
            this.manager = new RecentChatList("conv_id")
            this.refresh()
        },
        loadFull,
        async loadFromDB() {
            const chats = await getChatsFromDB()
            if (chats.length > 0) {
                this.rebuildFrom(chats)
            }
        },
        async loadPartial() {
            await this.loadFromDB()
            const partialStates = getJsonScriptData('partial_states') ?? []
            if (partialStates.length > 0) {
                this.rebuildFrom(partialStates)
                await putChatsToDB(partialStates)
            }
        },
        put(conv) {
            this.manager.upsertToFront(conv)
            this.refresh()
        },
        refresh() {
            this.conversations = this.manager.toArray()
            this.totalUnread = this.conversations.reduce((acc, cur) => acc + cur.unread, 0)
        },
        rebuildFrom(states) {
            this.manager.rebuildFromSortedArray(states)
            this.refresh()
        }
    })
    const store = Alpine.store(chatStoreName)
    store.init()
    return store
}

function setupFriendStore(alpine) {
    const friendStoreName = 'friends'
    Alpine.store(friendStoreName, {
        friends: [],
        friendMap: {},
        init() {
            this.loadFromDB()
        },
        async loadFromDB() {
            const friends = await getFriendsFromDB()
            if (friends.length > 0) {
                this.setFriends(friends)
            }
        },
        setFriends(data) {
            this.friends = []
            this.friendMap = {}
            for (const item of data) {
                this.friends.push(item)
                this.friendMap[item.id] = item
            }
        },
        getFriend(id) {
            return this.friendMap[id]
        }
    })
    const store = Alpine.store(friendStoreName)
    store.init()
    return store
}

export const chatStore = setupChatStore()
export const friendStore = setupFriendStore()
