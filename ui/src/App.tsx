import React from 'react';
import Popup from 'reactjs-popup';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLink, faQuestionCircle } from '@fortawesome/free-solid-svg-icons';
import LoadMoreButton from './components/LoadMoreButton';

interface Packet {
    distance: string,
    duplicates: number,
    imgPath: string,
    refURL: string,
    sources: string[],
}

interface Props { }

interface State {
    fetching: boolean,
    packets: Array<Packet>,
    pageNumber: number,
    srcImage: string,
}

class App extends React.Component<Props, State> {
    state: State = {
        fetching: true,
        packets: [],
        pageNumber: 1,
        srcImage: '',
    };

    getReferenceURL(): string {
        const { protocol, host } = window.location;
        return protocol + '//' + host;
    }

    private getBaseURL(pageNumber: number = 1): string {
        const { pathname, protocol, host } = window.location;
        let path = pathname.slice(1);
        if (path.length === 0) {
            path = this.state.srcImage;
        }
        const QUERY = '?pageNumber=' + pageNumber;
        const BASE = protocol + '//' + host + '/gen/' + path;
        const URL = BASE + QUERY;
        console.log(URL);
        return URL;
    }

    componentDidMount() {
        const URL = this.getBaseURL();
        this.fetchData(URL);
    }

    fetchData(URL: string): void {
        fetch(URL)
            .then(_ => _.json())
            .then(res => {
                console.log(res);
                const { sample, srcImage } = res;
                this.setState({ fetching: false, packets: sample, srcImage });
            })
            .catch(e => {
                console.log(e);
                this.setState({ fetching: false });
            });
    }

    loadMore() {
        const URL = this.getBaseURL(this.state.pageNumber + 1);
        this.setState(({ pageNumber }) => ({ pageNumber: pageNumber + 1 }));

        this.fetchData(URL);
    }

    render() {
        const { fetching, packets } = this.state;

        if (fetching === true) {
            return null;
        }

        const getBadge = (num_refs: number) => (
            <span className="notify-badge top left blue cursor">
                {num_refs} <FontAwesomeIcon icon={faLink} />
            </span>
        );

        const learnMore = (
            <span className="cursor">
                <FontAwesomeIcon icon={faQuestionCircle} size="2x"/>
            </span>
        );

        const description = `Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt
            ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi 
            ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum 
            dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia 
            deserunt mollit anim id est laborum`;
        
        return (
            <div>
                <div className="learn-more-container">
                    <Popup trigger={learnMore} modal>
                        <div className="learn-more">
                            <h2>What is this?</h2>
                            {description}
                        </div>
                    </Popup>
                </div>
                {
                    packets.map(packet => (
                        <div className="search-result" key={packet.imgPath}>
                            <Popup trigger={getBadge(packet.sources.length)} position="left center" modal>
                                <div>
                                    <ul>
                                        {packet.sources.map(source => {
                                            const wayback_machine_URL = 'http://web.archive.org/web/200910010000/' + source;

                                            return (
                                                <li key={source}>
                                                    <a href={wayback_machine_URL} rel="noopener noreferrer" target='_blank'>{source}</a>
                                                </li>
                                            );
                                        })}
                                    </ul>
                                </div>
                            </Popup>
                            <a href={packet.refURL}>
                                <span className="notify-badge top right red">{packet.duplicates + "x"}</span>
                                <img key={packet.imgPath} src={packet.imgPath} alt={packet.imgPath} />
                            </a>
                        </div>
                    ))
                }
                <LoadMoreButton onAction={() => this.loadMore()} />
            </div>
        );
    }
}

export default App;
