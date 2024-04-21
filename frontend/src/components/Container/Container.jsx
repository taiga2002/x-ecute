import { TopTIcon } from '../Sidebar/İcons';
import TweetBox from '../TweetBox/TweetBox';
import Tweets from '../Tweets/Tweets';

export default function ContainerPage() {

    const tweetData = [
        {
            bodyText: "Happy 4/20!!",
            image: "https://live.staticflickr.com/833/26744043367_4420fbb9f2_b.jpg",
            timeAgo: "20m",
            display: true,
            likeCount: 10,
            retweetCount: 3,
            replyCount: 1,
            shareCount: 8,
            username: "@taiga2002",
            displayName: "Taiga-san",
            profilePicture: "https://media.licdn.com/dms/image/D4D03AQGdNjaadS0EXQ/profile-displayphoto-shrink_200_200/0/1686292792185?e=2147483647&v=beta&t=t45oUYtA8T9YzN7QtOWxI7yAPzPP443MfqV76PjZv18",
            verified: true,
            animation: true
        },
        {
            bodyText: "I love Rust!!!",
            image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbTqpMnn87gJ957p_S4ttQeVPunbXHGlwxeBNC4hgWmg&s",
            timeAgo: "59m",
            display: true,
            likeCount: 25,
            retweetCount: 7,
            replyCount: 0,
            shareCount: 7,
            username: "@rohank2003",
            displayName: "Reddy",
            profilePicture: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzwIc_FElUS4_wkZF3uUljZ20dDd_xwMwOQZkXR_v8oA&s",
            animation: false,
        },
        
    ]
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
                    <img className="rounded-full h-11 w-11 mt-1" src="https://pbs.twimg.com/profile_images/1439646648410464258/C52zZ4ff_400x400.jpg"/>
                    <TweetBox/>
            </div>
            <div>
                {tweetData.map(data => (
                    <Tweets info={data}/>
                ))}
            </div>
        </>
    )
}