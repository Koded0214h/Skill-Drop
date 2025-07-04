// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SkillBadgeNFT is ERC721, Ownable {
    uint256 public nextTokenId;

    constructor(address initialOwner) ERC721("SkillBadge", "SBDG") Ownable(initialOwner) {}

    function mintBadge(address recipient) external onlyOwner {
        _safeMint(recipient, nextTokenId);
        nextTokenId++;
    }
}
