import { Reply, Retweet, Like, Share, VerifiedBadge } from '../Sidebar/İcons';
import { useState, useEffect } from 'react';

export default function Tweets(props){
    const [info, setInfo] = useState({});

    useEffect(() => setInfo(props.info), []);
    return(
        <>
        <div className="flex space-x-3 px-4 py-3 border-b border-primary-container_border_color">
            <img src={info.profilePicture} className="w-11 h-11 rounded-full" />
            <div className="flex-1">
                <div className="flex items-center text-sm space-x-2">
                <span className="ml-1 font-bold text-white">{info.displayName} <VerifiedBadge isVerified={info.verified}/></span>
                <span className="ml-2 text-primary-gray_colors">{info.username}</span>
                <div className="mx-2 text-primary-gray_colors">·</div>
                <span className="text-primary-gray_colors">{info.timeAgo}</span>
                </div>
                <div className="ml-1">
                    <p className="items-center text-white overflow-hidden">
                        {info.bodyText}
                        <img className="mt-3 rounded-xl" src={info.image}/>
                    </p>
                    <ul className="flex justify-between mt-2">
                        <li className="flex items-center space-x-3 text-primary-gray_colors text-sm group">
                            <div className="flex items-center justify-center w-9 h-9 rounded-full transform transition-colors duration-2 group-hover:bg-primary-tweets_hover_colors1 cursor-pointer">
                                <Reply/>
                            </div>
                            <span>{info.replyCount}</span>
                        </li>

                        <li className="flex items-center space-x-3 text-primary-gray_colors text-sm group">
                            <div className="flex items-center justify-center w-9 h-9 rounded-full transform transition-colors duration-2 group-hover:bg-primary-tweets_hover_colors2 cursor-pointer">
                                <Retweet/>
                            </div>
                            <span>{info.retweetCount}</span>
                        </li>

                        <li className="flex items-center space-x-3 text-primary-gray_colors text-sm group">
                            <div className="flex items-center justify-center w-9 h-9 rounded-full transform transition-colors duration-2 group-hover:bg-primary-tweets_hover_colors3 cursor-pointer">
                                <Like/>
                            </div>
                            <span>{info.likeCount}</span>
                        </li>

                        <li className="flex items-center space-x-3 text-primary-gray_colors text-sm group">
                            <div className="flex items-center justify-center w-9 h-9 rounded-full transform transition-colors duration-2 group-hover:bg-primary-tweets_hover_colors1 cursor-pointer">
                                <Share/>
                            </div>
                            <span>{info.shareCount}</span>
                        </li>

                    </ul>
                </div>
            </div>
        </div>
        
        </>
    )
}