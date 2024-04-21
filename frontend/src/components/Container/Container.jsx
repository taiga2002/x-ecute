import { TopTIcon } from '../Sidebar/İcons';
import TweetBox from '../TweetBox/TweetBox';
import Tweets from '../Tweets/Tweets';
import { useState , useEffect } from 'react'

/* Sometimes need to run `export NODE_OPTIONS=--openssl-legacy-provider` */

export default function ContainerPage() {

    const [tweetData, setTweetData] = useState([]);
    const [userData, setUserData] = useState({});

    useEffect(() => {
        fetch('http://127.0.0.1:5000/tweets?user_id=elonmusk')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                setTweetData(data);
                console.log(data);
            })
            .catch(error => {
                // Handle errors
                console.error('There was a problem with the fetch operation:', error);
            });
        fetch('http://127.0.0.1:5000/user')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                setUserData(data);
                console.log(data);
            })
            .catch(error => {
                // Handle errors
                console.error('There was a problem with the fetch operation:', error);
            });
    }, []);

    // const tweetData = [
    //     {
    //         bodyText: "Happy 4/20!!",
    //         image: "https://pbs.twimg.com/media/GLoiWIbawAALYK4?format=jpg&name=4096x4096",
    //         timeAgo: "20m",
    //         display: true,
    //         likeCount: 10,
    //         retweetCount: 3,
    //         replyCount: 1,
    //         shareCount: 8,
    //         username: "@taiga2002",
    //         displayName: "Taiga-san",
    //         profilePicture: "https://media.licdn.com/dms/image/D4D03AQGdNjaadS0EXQ/profile-displayphoto-shrink_200_200/0/1686292792185?e=2147483647&v=beta&t=t45oUYtA8T9YzN7QtOWxI7yAPzPP443MfqV76PjZv18",
    //         verified: true,
    //         rocket_launch: false,
    //         valentine: false
    //     },
    //     {
    //         bodyText: "I love Rust!!!",
    //         image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbTqpMnn87gJ957p_S4ttQeVPunbXHGlwxeBNC4hgWmg&s",
    //         timeAgo: "59m",
    //         display: true,
    //         likeCount: 25,
    //         retweetCount: 7,
    //         replyCount: 0,
    //         shareCount: 7,
    //         username: "@rohank2003",
    //         displayName: "Reddy",
    //         profilePicture: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzwIc_FElUS4_wkZF3uUljZ20dDd_xwMwOQZkXR_v8oA&s",
    //         rocket_launch: false,
    //         valentine: true
    //     },
    // ]

    return(
        <>
            <header className="sticky-top flex justify-between items-center p-4 border-b border-primary-container_border_color bg-black">
                <span className="font-bold text-xl text-white">Home</span>
                <div className="flex items-center justify-center w-9 h-9 rounded-full transform transition-colors duration-2 hover:bg-gray-700 hover:bg-opacity-70 cursor-pointer">
                    <a title="Top Tweets">
                        <TopTIcon/>
                    </a>
                </div>
            </header>
            <div className="flex space-x-4 px-5 py-2 border-b border-primary-container_border_color">
                    <img className="rounded-full h-11 w-11 mt-1" src={userData.profilePicture}/>
                    <TweetBox/>
            </div>
            <div>
                {tweetData.map(data => (
                    <Tweets key={data.id} info={data} />
                ))}
            </div>
        </>
    )
}