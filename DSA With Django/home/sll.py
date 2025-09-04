class Node:
    def __init__(self, data=None, link=None):
        self.data = data
        self.link = link
        
class SLL:
    def __init__(self, head=None):
        self.head = head
        self.tail = None
        self.size = 0

    def is_empty(self):
        return self.head == None

    def insert_at_start(self, data):
        new_node = Node(data, self.head)
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self.size += 1
        return new_node

    def insert_at_end(self, data):
        new_node = Node(data, None)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.link = new_node
            self.tail = new_node
        self.size += 1
        return new_node

    def insert_after(self, temp, data):
        if temp is not None:
            new_node = Node(data, temp.link)
            temp.link = new_node
            if temp == self.tail:
                self.tail = new_node
            self.size += 1
            return new_node
        return None

    def insert_at_position(self, position, data):
        if position <= 0:
            return self.insert_at_start(data)
        elif position >= self.size:
            return self.insert_at_end(data)
        
        temp = self.head
        for _ in range(position - 1):
            temp = temp.link
        
        return self.insert_after(temp, data)

    def search(self, data):
        temp = self.head
        while temp is not None:
            if temp.data == data:
                return temp
            temp = temp.link
        return None

    def search_by_id(self, link_id):
        temp = self.head
        while temp is not None:
            if temp.data.link_id == link_id:
                return temp
            temp = temp.link
        return None

    def print_list(self):
        temp = self.head
        while temp is not None:
            print(temp.data, end=' ')
            temp = temp.link

    def delete_first(self):
        if self.head is not None:
            deleted_node = self.head
            self.head = self.head.link
            if self.head is None:
                self.tail = None
            self.size -= 1
            return deleted_node
        return None

    def delete_last(self):
        if self.head is None:
            return None
        elif self.head.link is None:
            deleted_node = self.head
            self.head = None
            self.tail = None
            self.size -= 1
            return deleted_node
        else:
            temp = self.head
            while temp.link.link is not None:
                temp = temp.link
            deleted_node = temp.link
            temp.link = None
            self.tail = temp
            self.size -= 1
            return deleted_node

    def delete_item(self, data):
        if self.head is None:
            return None
        elif self.head.data == data:
            return self.delete_first()
        else:
            temp = self.head
            while temp.link is not None:
                if temp.link.data == data:
                    deleted_node = temp.link
                    temp.link = temp.link.link
                    if temp.link is None:
                        self.tail = temp
                    self.size -= 1
                    return deleted_node
                temp = temp.link
        return None

    def delete_by_id(self, link_id):
        if self.head is None:
            return None
        elif self.head.data.link_id == link_id:
            return self.delete_first()
        else:
            temp = self.head
            while temp.link is not None:
                if temp.link.data.link_id == link_id:
                    deleted_node = temp.link
                    temp.link = temp.link.link
                    if temp.link is None:
                        self.tail = temp
                    self.size -= 1
                    return deleted_node
                temp = temp.link
        return None

    def is_full(self):
        return False
    
    def list_count(self):
        return self.size
    
    def destroy_list(self):
        self.head = None
        self.tail = None
        self.size = 0

    def retrieve_nth_node(self, n):
        if n < 0 or n >= self.size:
            return None
        
        temp = self.head
        count = 0
        
        while temp is not None:
            if count == n:
                return temp.data
            temp = temp.link
            count += 1
        
        return None

    def to_list(self):
        result = []
        temp = self.head
        while temp is not None:
            result.append(temp.data)
            temp = temp.link
        return result

    def find_position_by_id(self, link_id):
        temp = self.head
        position = 0
        while temp is not None:
            if temp.data.link_id == link_id:
                return position
            temp = temp.link
            position += 1
        return -1