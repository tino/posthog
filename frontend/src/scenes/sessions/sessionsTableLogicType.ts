// Auto-generated with kea-typegen. DO NOT EDIT!

export interface sessionsTableLogicType {
    key: any
    actionCreators: {
        loadSessions: (
            selectedDate: any
        ) => {
            type: 'load sessions (frontend.src.scenes.sessions.sessionsTableLogic)'
            payload: any
        }
        loadSessionsSuccess: (
            sessions: never[]
        ) => {
            type: 'load sessions success (frontend.src.scenes.sessions.sessionsTableLogic)'
            payload: {
                sessions: never[]
            }
        }
        loadSessionsFailure: (
            error: string
        ) => {
            type: 'load sessions failure (frontend.src.scenes.sessions.sessionsTableLogic)'
            payload: {
                error: string
            }
        }
        setOffset: (
            offset: any
        ) => {
            type: 'set offset (frontend.src.scenes.sessions.sessionsTableLogic)'
            payload: { offset: any }
        }
        fetchNextSessions: () => {
            type: 'fetch next sessions (frontend.src.scenes.sessions.sessionsTableLogic)'
            payload: {
                value: boolean
            }
        }
        appendNewSessions: (
            sessions: any
        ) => {
            type: 'append new sessions (frontend.src.scenes.sessions.sessionsTableLogic)'
            payload: { sessions: any }
        }
        dateChanged: (
            date: any
        ) => {
            type: 'date changed (frontend.src.scenes.sessions.sessionsTableLogic)'
            payload: { date: any }
        }
        setDate: (
            date: any
        ) => {
            type: 'set date (frontend.src.scenes.sessions.sessionsTableLogic)'
            payload: { date: any }
        }
    }
    actionKeys: {
        'load sessions (frontend.src.scenes.sessions.sessionsTableLogic)': 'loadSessions'
        'load sessions success (frontend.src.scenes.sessions.sessionsTableLogic)': 'loadSessionsSuccess'
        'load sessions failure (frontend.src.scenes.sessions.sessionsTableLogic)': 'loadSessionsFailure'
        'set offset (frontend.src.scenes.sessions.sessionsTableLogic)': 'setOffset'
        'fetch next sessions (frontend.src.scenes.sessions.sessionsTableLogic)': 'fetchNextSessions'
        'append new sessions (frontend.src.scenes.sessions.sessionsTableLogic)': 'appendNewSessions'
        'date changed (frontend.src.scenes.sessions.sessionsTableLogic)': 'dateChanged'
        'set date (frontend.src.scenes.sessions.sessionsTableLogic)': 'setDate'
    }
    actionTypes: {
        loadSessions: 'load sessions (frontend.src.scenes.sessions.sessionsTableLogic)'
        loadSessionsSuccess: 'load sessions success (frontend.src.scenes.sessions.sessionsTableLogic)'
        loadSessionsFailure: 'load sessions failure (frontend.src.scenes.sessions.sessionsTableLogic)'
        setOffset: 'set offset (frontend.src.scenes.sessions.sessionsTableLogic)'
        fetchNextSessions: 'fetch next sessions (frontend.src.scenes.sessions.sessionsTableLogic)'
        appendNewSessions: 'append new sessions (frontend.src.scenes.sessions.sessionsTableLogic)'
        dateChanged: 'date changed (frontend.src.scenes.sessions.sessionsTableLogic)'
        setDate: 'set date (frontend.src.scenes.sessions.sessionsTableLogic)'
    }
    actions: {
        loadSessions: (selectedDate: any) => void
        loadSessionsSuccess: (sessions: never[]) => void
        loadSessionsFailure: (error: string) => void
        setOffset: (offset: any) => void
        fetchNextSessions: () => void
        appendNewSessions: (sessions: any) => void
        dateChanged: (date: any) => void
        setDate: (date: any) => void
    }
    cache: Record<string, any>
    connections: any
    constants: any
    defaults: any
    events: any
    path: ['frontend', 'src', 'scenes', 'sessions', 'sessionsTableLogic']
    pathString: 'frontend.src.scenes.sessions.sessionsTableLogic'
    propTypes: any
    props: Record<string, any>
    reducer: (
        state: any,
        action: () => any,
        fullState: any
    ) => {
        sessions: never[]
        sessionsLoading: boolean
        isLoadingNext: boolean
        offset: null
        selectedDate: Moment
    }
    reducerOptions: any
    reducers: {
        sessions: (state: never[], action: any, fullState: any) => never[]
        sessionsLoading: (state: boolean, action: any, fullState: any) => boolean
        isLoadingNext: (state: boolean, action: any, fullState: any) => boolean
        offset: (state: null, action: any, fullState: any) => null
        selectedDate: (state: Moment, action: any, fullState: any) => Moment
    }
    selector: (
        state: any
    ) => {
        sessions: never[]
        sessionsLoading: boolean
        isLoadingNext: boolean
        offset: null
        selectedDate: Moment
    }
    selectors: {
        sessions: (state: any, props: any) => never[]
        sessionsLoading: (state: any, props: any) => boolean
        isLoadingNext: (state: any, props: any) => boolean
        offset: (state: any, props: any) => null
        selectedDate: (state: any, props: any) => Moment
        selectedDateURLparam: (state: any, props: any) => any
    }
    values: {
        sessions: never[]
        sessionsLoading: boolean
        isLoadingNext: boolean
        offset: null
        selectedDate: Moment
        selectedDateURLparam: any
    }
    _isKea: true
    __keaTypeGenInternalSelectorTypes: {
        selectedDateURLparam: (arg1: any) => any
    }
}
