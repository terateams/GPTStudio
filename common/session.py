import uuid

import streamlit as st


class PageSessionState:
    def __init__(self, prefix):
        self._prefix = prefix
        self.initn_attr("session_id", f"{prefix}{uuid.uuid4()}")

    def initn_attr(self, key: str, default_value: object):
        if not hasattr(st.session_state, self.getkey(key)):
            st.session_state[self.getkey(key)] = default_value

    def add_list_item(self, key: str, value: object):
        if not hasattr(st.session_state, self.getkey(key)):
            st.session_state[self.getkey(key)] = []
        try:
            st.session_state[self.getkey(key)].append(value)
        except:
            raise AttributeError("Cannot append to non-list attribute")

    def update_last_list_item(self, key: str, value: object):
        if not hasattr(st.session_state, self.getkey(key)):
            st.session_state[self.getkey(key)] = []
            st.session_state[self.getkey(key)].append(value)
            return
        try:
            st.session_state[self.getkey(key)][-1] = value
        except:
            raise AttributeError("Cannot update last list item")

    def add_chat_msg(self, key: str, value: object):
        if not hasattr(st.session_state, self.getkey(key)):
            st.session_state[self.getkey(key)] = []
        try:
            st.session_state[self.getkey(key)].append(value)
        except:
            raise AttributeError("Cannot append to non-list attribute")

    def update_last_msg(self, key: str, value: object):
        if not hasattr(st.session_state, self.getkey(key)):
            st.session_state[self.getkey(key)] = []
            st.session_state[self.getkey(key)].append(value)
            return
        try:
            st.session_state[self.getkey(key)][-1] = value
        except:
            raise AttributeError("Cannot update last message")

    def __getattr__(self, key):
        if key == "_prefix":
            return self.__dict__[key]
        if self.getkey(key) in st.session_state:
            return st.session_state[self.getkey(key)]
        else:
            return None

    def __setattr__(self, key, value):
        if key == "_prefix":
            self.__dict__[key] = value
        else:
            st.session_state[self.getkey(key)] = value

    def __delattr__(self, key):
        if key == "_prefix":
            raise AttributeError("Cannot delete _prefix attribute")
        st.session_state.pop(self.getkey(key), None)

    def __contains__(self, key):
        return self.getkey(key) in st.session_state

    def __getitem__(self, key):
        if key == "_prefix":
            return self.__dict__[key]
        return st.session_state[self.getkey(key)]

    def __setitem__(self, key, value):
        if key == "_prefix":
            self.__dict__[key] = value
        else:
            st.session_state[self.getkey(key)] = value

    def __delitem__(self, key):
        if key == "_prefix":
            raise AttributeError("Cannot delete _prefix attribute")
        st.session_state.pop(self.getkey(key), None)

    def __len__(self):
        return len(st.session_state)

    def __iter__(self):
        return iter(st.session_state)

    def __repr__(self):
        return repr(st.session_state)

    def __str__(self):
        return str(st.session_state)

    def getkey(self, key):
        return f"{self._prefix}_{key}"
