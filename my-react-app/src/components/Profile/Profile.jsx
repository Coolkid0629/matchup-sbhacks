import React, { useState, useEffect } from 'react';
import "./Profile.css"

const ProfilePage = () => {
  const [profileImage, setProfileImage] = useState(null);
  const [error, setError] = useState(null);
  const imageEndpoint = 'https://randomuser.me/api/'; 
  useEffect(() => {
    // Fetch the profile image when the component loads
    const fetchProfileImage = async () => {
      try {
        const response = await fetch(imageEndpoint);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log(data.results[0])
        setProfileImage(data.results[0].picture.large);
      } catch (err) {
        setError('Failed to load profile image.');
        console.error(err);
      }
    };

    fetchProfileImage();

    // Cleanup function to revoke object URL when component unmounts
    return () => {
      if (profileImage) URL.revokeObjectURL(profileImage);
    };
  }, []); // Empty dependency array ensures this only runs on mount

  return (
    <div className="profile-container">
      <h1 className="profile-header">Profile Page</h1>
      {error ? (
        <p className="profile-error">{error}</p>
      ) : profileImage ? (
        <img
          src={profileImage}
          alt="Profile"
          className="profile-image"
        />
      ) : (
        <p className="profile-loading">Loading image...</p>
      )}
    </div>
  );
};

export default ProfilePage;
