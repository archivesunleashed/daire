import React from 'react';

interface Packet {
    distance: string,
    imgPath: string,
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

    componentDidMount() {
        const URL = window.location.href + 'gen'
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
                        <img key={packet.imgPath} src={packet.imgPath} />
                    ))
                }
            </div>
        );
    }
}

export default App;
