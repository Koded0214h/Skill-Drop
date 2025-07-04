const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners(); // Get deployer address

  const Contract = await hre.ethers.getContractFactory("SkillBadgeNFT");
  const contract = await Contract.deploy(deployer.address);  // Pass initialOwner to Ownable

  await contract.waitForDeployment();  // Updated for Ethers v6+

  console.log("SkillBadgeNFT deployed to:", await contract.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
