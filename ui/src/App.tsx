import React from 'react';

interface Packet {
    distance: string,
    duplicates: number,
    imgPath: string,
    refURL: string,
}

interface Props { }

interface State {
    fetching: boolean;
    packets: Array<Packet>
}

class App extends React.Component<Props, State> {
    state: State = {
        fetching: true,
        packets: [],
    }

    getReferenceURL(): string {
        const { protocol, host } = window.location
        return protocol + '//' + host
    }

    componentDidMount() {
        const { pathname, protocol, host } = window.location
        const path = pathname.slice(1)

        const URL = protocol + '//' + host + '/gen/' + path

        console.log(URL)

        fetch(URL)
            .then(_ => _.json())
            .then(res => {
                console.log(res)
                this.setState({ fetching: false, packets: res.sample })
            })
            .catch(e => {
                console.log(e);
                this.setState({ fetching: false })
                // this.setState({ ...this.state, isFetching: false });
            });
    }

    render() {
        if (this.state.fetching === true) {
            return null;
        }

        return (
            <div >
                {
                    this.state.packets.map(packet => (
                        <div className="search-result">
                        <a href={packet.refURL}>
                        <span className="notify-badge">{packet.duplicates+"x"}</span>
                        <img key={packet.imgPath} src={packet.imgPath} />
                        </a>
                        </div>
                    ))
                }
            </div>
        );
    }
}

export default App;
