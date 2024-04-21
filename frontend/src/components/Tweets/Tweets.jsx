import { Reply, Retweet, Like, Share, VerifiedBadge } from '../Sidebar/İcons';
import { useState, useEffect, useRef } from 'react';
import Heart from "react-animated-heart";
import styles from './Tweets.module.css';

export default function Tweets(props){
    const [info, setInfo] = useState({});
    const [showHeart, setShowHeart] = useState(false);
    const [explodeHeart, setExplodeHeart] = useState(false);
    const [componentClass, setComponentClass] = useState("");

    useEffect(() => {
        if (props.info.rocket_launch) {
            setComponentClass(styles.flyaway);
        } else if (props.info.valentine) {
            setComponentClass(styles.explode);
        }
        setInfo(props.info);
    }, []);

    useEffect(() => {
        if (info.valentine) {
            const timer = setTimeout(() => {
                setShowHeart(true);
                const explodeTimer = setTimeout(() => {
                    setExplodeHeart(true);
                    setTimeout(() => {
                        setShowHeart(false);
                        setComponentClass("");
                    }, 3000);
                }, 10);
                return () => clearTimeout(explodeTimer); // Cleanup function to clear the inner setTimeout
            }, 3000);
            return () => clearTimeout(timer); // Cleanup function to clear the outer setTimeout
        }
    }, [info.valentine]);

    return(
        <div style={{"display": props.info.display ? "block" : "none"}}>
            { info.valentine && showHeart ? 
                <div className="flex justify-center border-b border-primary-container_border_color">
                    <Heart isClick={explodeHeart} className="justify-center" />
                    <Heart isClick={explodeHeart} className="justify-center" />
                    <Heart isClick={explodeHeart} className="justify-center" />
                    <Heart isClick={explodeHeart} className="justify-center" />
                </div>
                :
                <div className = {componentClass}>
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
                                <p className="items-center text-white overflow-auto">
                                    {info.bodyText && (
                                        <span dangerouslySetInnerHTML={{ __html: info.bodyText.replace(/\n/g, '<br>').replace(/ /g, '&nbsp;') }} />
                                    )}
                                    {info.image && <img className="mt-3 rounded-xl" src={info.image} alt="Info Image" />}
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
                </div> }
        </div>
    )
}