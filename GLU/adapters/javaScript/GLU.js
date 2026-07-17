const events = {};


export function emit(name, data) {
    if (events[name]) {
        events[name].forEach(
            callback => callback(data)
        );
    }
}
